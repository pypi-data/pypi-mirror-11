from . import catalogs
from . import importers
from babel import util as babel_util
from babel.messages import extract
from babel.messages import pofile
from grow.common import utils
from grow.pods import messages
import collections
import os
import tokenize


_TRANSLATABLE_EXTENSIONS = (
  '.html',
  '.md',
  '.yaml',
  '.yml',
)



class Catalogs(object):
  root = '/translations'

  def __init__(self, pod):
    self.pod = pod
    self.template_path = os.path.join(Catalogs.root, 'messages.pot')

  def get(self, locale, basename='messages.po'):
    return catalogs.Catalog(basename, locale, pod=self.pod)

  def get_template(self, basename='messages.pot'):
    return catalogs.Catalog(basename, None, pod=self.pod)

  def list_locales(self):
    locales = set()
    for path in self.pod.list_dir(Catalogs.root):
      parts = path.split('/')
      if len(parts) > 2:
        locales.add(parts[1])
    return list(locales)

  def __iter__(self):
    for locale in self.list_locales():
      yield self.get(locale)

  def compile(self):
    locales = self.list_locales()
    for locale in locales:
      catalog = self.get(locale)
      if not catalog.exists:
        self.pod.logger.info('Does not exist: {}'.format(catalog))
        continue
      catalog.compile()

  def to_message(self):
    message = messages.CatalogsMessage()
    message.catalogs = []
    for locale in self.list_locales():
      catalog = self.get(locale)
      message.catalogs.append(catalog.to_message())
    return message

  def init(self, locales):
    for locale in locales:
      catalog = self.get(locale)
      catalog.init(template_path=self.template_path)

  def update(self, locales, use_fuzzy=False):
    for locale in locales:
      catalog = self.get(locale)
      catalog.update(template_path=self.template_path, use_fuzzy=use_fuzzy)

  def import_translations(self, path, locale=None):
    importer = importers.Importer(self.pod)
    importer.import_path(path, locale=locale)

  def extract_missing(self, locales, out_path, use_fuzzy=False):
    messages_to_locales = collections.defaultdict(list)
    for locale in locales:
      catalog = self.get(locale)
      missing_messages = catalog.list_missing(use_fuzzy=use_fuzzy)
      text = 'Extracted missing strings: {} ({}/{})'
      num_missing = len(missing_messages)
      num_total = len(catalog)
      self.pod.logger.info(text.format(catalog.locale, num_missing, num_total))
      for message in missing_messages:
        messages_to_locales[message].append(catalog.locale)
    self.pod.create_file(out_path, None)
    babel_catalog = pofile.read_po(self.pod.open_file(out_path))
    for message in messages_to_locales.keys():
      babel_catalog[message.id] = message
    self.write_template(out_path, babel_catalog)

  def _get_or_create_catalog(self, template_path):
    exists = True
    if not self.pod.file_exists(template_path):
      self.pod.create_file(template_path, None)
      exists = False
    catalog = pofile.read_po(self.pod.open_file(template_path))
    return catalog, exists

  def _add_message(self, catalog, message):
    lineno, string, comments, context = message
    flags = set()
    if string in catalog:
      existing_message = catalog.get(string)
      flags = existing_message.flags
    return catalog.add(string, None, auto_comments=comments, context=context,
                       flags=flags)

  def extract(self, include_obsolete=False):
    env = self.pod.create_template_env()
    template_path = self.template_path
    catalog_obj, exists = self._get_or_create_catalog(template_path)

    if not include_obsolete:
      catalog_obj.obsolete = babel_util.odict()
      for message in list(catalog_obj):
        catalog_obj.delete(message.id, context=message.context)

    extracted = []

    comment_tags = [
        ':',
    ]
    options = {
        'extensions': ','.join(env.extensions.keys()),
        'silent': 'false',
    }
    # Extract messages from content and views.
    pod_files = [os.path.join('/views', path) for path in self.pod.list_dir('/views/')]
    pod_files += [os.path.join('/content', path) for path in self.pod.list_dir('/content/')]
    for pod_path in pod_files:
      if os.path.splitext(pod_path)[-1] in _TRANSLATABLE_EXTENSIONS:
        self.pod.logger.info('Extracting from: {}'.format(pod_path))
        fp = self.pod.open_file(pod_path)
        try:
          messages = extract.extract('jinja2.ext.babel_extract', fp,
                                     options=options, comment_tags=comment_tags)
          for message in messages:
            added_message = self._add_message(catalog_obj, message)
            extracted.append(added_message)
        except tokenize.TokenError:
          self.pod.logger.error('Problem extracting: {}'.format(pod_path))
          raise

    # Extract messages from content files.
    def callback(doc, item, key, unused_node):
      # Verify that the fields we're extracting are fields for a document that's
      # in the default locale. If not, skip the document.
      _handle_field(doc.pod_path, item, key, unused_node)

    def _handle_field(path, item, key, node):
      if not key.endswith('@') or not isinstance(item, basestring):
        return
      # Support gettext "extracted comments" on tagged fields. This is
      # consistent with extracted comments in templates, which follow
      # the format "{#: Extracted comment. #}". An example:
      #   field@: Message.
      #   field@#: Extracted comment for field@.
      auto_comments = []
      if isinstance(node, dict):
        auto_comment = node.get('{}#'.format(key))
        if auto_comment:
          auto_comments.append(auto_comment)
      added_message = catalog_obj.add(item, None, auto_comments=auto_comments)
      if added_message not in extracted:
        extracted.append(added_message)

    for collection in self.pod.list_collections():
      self.pod.logger.info('Extracting from collection: {}'.format(collection.pod_path))
      for doc in collection.list_documents(include_hidden=True):
        tagged_fields = doc.get_tagged_fields()
        utils.walk(tagged_fields, lambda *args: callback(doc, *args))

    # Extract messages from podspec.
    config = self.pod.get_podspec().get_config()
    podspec_path = '/podspec.yaml'
    self.pod.logger.info('Extracting from podspec: {}'.format(podspec_path))
    utils.walk(config, lambda *args: _handle_field(podspec_path, *args))

    # Write to PO template.
    return self.write_template(template_path, catalog_obj,
                               include_obsolete=include_obsolete)

  def write_template(self, template_path, catalog, include_obsolete=False):
    template_file = self.pod.open_file(template_path, mode='w')
    pofile.write_po(template_file, catalog, width=80, omit_header=True,
                    sort_output=True, sort_by_file=True,
                    ignore_obsolete=(not include_obsolete))
    text = 'Wrote {} messages to translation template: {}'
    self.pod.logger.info(text.format(len(catalog), template_path))
    template_file.close()
    return catalog
