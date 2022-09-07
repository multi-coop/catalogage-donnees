// Source: https://unpkg.com/browse/snarkdown@2.0.0/dist/snarkdown.modern.js
import snarkdown from "@js/snarkdown.js";

export const renderMarkdown = (content: string): string => {
  return snarkdown(content);
};
