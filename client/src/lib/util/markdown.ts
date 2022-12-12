import { marked } from "marked";
export const renderMarkdown = (content: string): string => {
  const renderer = new marked.Renderer();

  // This method add the attribute "target _blank" to each link redirecting to an external host
  // See https://github.com/markedjs/marked/issues/655#issuecomment-712380889
  const linkRenderer = renderer.link;
  renderer.link = (href, title, text) => {
    if (!href) {
      return text;
    }
    const localLink = href.startsWith(
      `${location.protocol}//${location.hostname}`
    );
    const html = linkRenderer.call(renderer, href, title, text);
    return localLink
      ? html
      : html.replace(
          /^<a /,
          `<a target="_blank" rel="noreferrer noopener nofollow" `
        );
  };
  return marked(content, { renderer });
};
