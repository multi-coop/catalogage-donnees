/**
 * Browsers (tested on Chrome and Firefox) consider the browser landing page (the page opened when you start the browser) as the first page
 * in the history.
 * Here we check if the user has visited at least one page more than this landing page
 *
 */

export const hasHistory = (): boolean => window && window.history.length > 2;
