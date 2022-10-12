import { derived, get, writable } from "svelte/store";
import type { Catalog } from "src/definitions/catalogs";
import { Maybe } from "$lib/util/maybe";
import { debounce } from "$lib/util/store";
import paths from "$lib/paths";
import { getCatalogBySiret } from "$lib/repositories/catalogs";
import { account, apiToken } from "../auth";

type NavItem = {
  label: string;
  href: string;
};

const currentCatalog = writable<Maybe<Catalog>>();

// XXX: Upon login, $account may be set a few times in a row.
// Make only one HTTP request once things have settled.
debounce(account, 100).subscribe((accountValue) => {
  if (!Maybe.Some(accountValue)) {
    currentCatalog.set(null);
    return;
  }

  getCatalogBySiret({
    fetch,
    apiToken: Maybe.expect(get(apiToken), "$apiToken"),
    siret: accountValue.organizationSiret,
  }).then((catalog) => {
    currentCatalog.set(catalog);
  });
});

export const navigationItems = derived(currentCatalog, (catalog): NavItem[] => {
  return [
    {
      label: "Accueil",
      href: paths.home,
    },
    {
      label: "Rechercher",
      href: paths.datasetSearch,
    },
    ...(Maybe.Some(catalog)
      ? [
          {
            label: "Contribuer",
            href: paths.contribute,
          },
        ]
      : []),
  ];
});
