<script lang="ts">
  import { page } from "$app/stores";
  import { apiToken, account } from "src/lib/stores/auth";
  import DatasetListTemplate from "src/lib/templates/DatasetListTemplate/DatasetListTemplate.svelte";

  import { getPageFromParams } from "src/lib/util/pagination";
  import { getDatasets } from "src/lib/repositories/datasets";
  import Spinner from "src/lib/components/Spinner/Spinner.svelte";
  import LandingTemplate from "src/lib/templates/LandingTemplate/LandingTemplate.svelte";

  let pageNumber = getPageFromParams($page.url.searchParams) || 1;
</script>

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

<style>
  .spinner-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 200px;
  }
</style>
