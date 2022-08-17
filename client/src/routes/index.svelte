<script lang="ts">
  import { page as pageStore } from "$app/stores";
  import type { Dataset } from "src/definitions/datasets";
  import type { Paginated } from "src/definitions/pagination";
  import { Maybe } from "$lib/util/maybe";
  import { apiToken, user } from "src/lib/stores/auth";
  import DatasetListTemplate from "src/lib/templates/DatasetListTemplate/DatasetListTemplate.svelte";
  import { beforeUpdate } from "svelte";

  import { getPageFromParams } from "src/lib/util/pagination";
  import { getDatasets } from "src/lib/repositories/datasets";
  import Spinner from "src/lib/components/Spinner/Spinner.svelte";

  let paginatedDatasets: Maybe<Paginated<Dataset>>;
  let page = 1;
  let loading = false;

  beforeUpdate(async () => {
    loading = true;
    if (Maybe.Some($user) && !Maybe.Some(paginatedDatasets)) {
      page = getPageFromParams($pageStore.url.searchParams);
      paginatedDatasets = await getDatasets({
        fetch,
        apiToken: $apiToken,
        page,
      });
    }
    loading = false;
  });
</script>

<svelte:head>
  <title>Catalogue</title>
</svelte:head>

{#if loading}
  <div class="spinner-container">
    <Spinner />
  </div>
{:else if Maybe.Some($user) && Maybe.Some(paginatedDatasets)}
  <DatasetListTemplate currentPage={page} {paginatedDatasets} />
{:else}
  <p>foo</p>
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
