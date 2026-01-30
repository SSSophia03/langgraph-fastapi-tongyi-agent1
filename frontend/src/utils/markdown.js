import MarkdownIt from 'markdown-it';

const md = new MarkdownIt({
  html: true,
  linkify: true
});

export function renderMarkdown(text) {
  return md.render(text || '');
}