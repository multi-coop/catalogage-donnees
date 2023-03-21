<script lang="ts">
  import { page } from "$app/stores";
  import { apiToken, account } from "src/lib/stores/auth";
  import DatasetListTemplate from "src/lib/templates/DatasetListTemplate/DatasetListTemplate.svelte";

  import { getPageFromParams } from "src/lib/util/pagination";
  import { getDatasets } from "src/lib/repositories/datasets";
  import Spinner from "src/lib/components/Spinner/Spinner.svelte";
  import LandingTemplate from "src/lib/templates/LandingTemplate/LandingTemplate.svelte";
  import SkipLink from "src/lib/components/SkipLink/SkipLink.svelte";
  import Header from "src/lib/components/Header/Header.svelte";
  import Footer from "src/lib/components/Footer/Footer.svelte";
  import type { Fetch } from "src/definitions/fetch";
  import type { Dataset } from "src/definitions/datasets";
  import type { Paginated } from "src/definitions/pagination";
  import type { Maybe } from "src/lib/util/maybe";
  import { getCatalogs } from "src/lib/repositories/catalogs";
  import type { Catalog } from "src/definitions/catalogs";

  let pageNumber = getPageFromParams($page.url.searchParams) || 1;

  const getDatasetsAndOrganizations = async (
    fetch: Fetch,
    apiToken: string
  ): Promise<[Maybe<Paginated<Dataset>>, Maybe<Catalog[]>]> => {
    // fetch datasets

    const datasets = await getDatasets({ fetch, apiToken, page: pageNumber });

    const catalogs = await getCatalogs({ fetch, apiToken });

    return [datasets, catalogs];
  };
</script>

<SkipLink
  linksMap={{
    "contenu principal": "contenu",
    "pied de page": "footer",
  }}
/>

<Header />

<!-- svelte-ignore a11y-no-redundant-roles -- this is the main page region. Here this role is not redundant -->
<main id="contenu" role="main">
  {#if $account}
    {#await getDatasetsAndOrganizations(fetch, $apiToken)}
      <div class="spinner-container">
        <Spinner />
      </div>
    {:then [paginatedDatasets, catalogs]}
      <DatasetListTemplate
        currentPage={pageNumber}
        {paginatedDatasets}
        {catalogs}
      />
    {/await}
  {:else}
    <LandingTemplate />
  {/if}
</main>

<Footer />

<style>
  .spinner-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 200px;
  }
</style>
