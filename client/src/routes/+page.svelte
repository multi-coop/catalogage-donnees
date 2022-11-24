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

  let pageNumber = getPageFromParams($page.url.searchParams) || 1;
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
    {#await getDatasets({ fetch, apiToken: $apiToken, page: pageNumber })}
      <div class="spinner-container">
        <Spinner />
      </div>
    {:then paginatedDatasets}
      <DatasetListTemplate currentPage={pageNumber} {paginatedDatasets} />
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
