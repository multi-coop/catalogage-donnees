import snarkdown from "snarkdown";

export const renderMarkdown = (content: string): string => {
  return snarkdown(content);
};
