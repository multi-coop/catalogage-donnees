export const buildMailToString = (
  adresses: string[],
  emailSubject: string,
  body: string
) => {
  const mailtoString = `mailto:${adresses.join(",")}?subject=${emailSubject}`;

  if (body) {
    return mailtoString.concat(`&body=${body}`);
  }

  return mailtoString;
};
