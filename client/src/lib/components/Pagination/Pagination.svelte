<script lang="ts">
  import type { GetPageLink } from "src/definitions/pagination";
  import { makePagination } from "$lib/util/pagination";

  export let currentPage: number;
  export let totalPages: number;
  export let getPageLink: GetPageLink;

  $: pagination = makePagination({ currentPage, totalPages, numSiblings: 2 });
</script>

<nav class="fr-pagination" aria-label="Pagination">
  <ul class="fr-pagination__list" data-testid="pagination-list">
    <li>
      <a
        class="fr-pagination__link fr-pagination__link--first"
        href={pagination.hasPrevious
          ? getPageLink(pagination.firstPage)
          : undefined}
        aria-disabled={!pagination.hasPrevious ? true : undefined}
        title="Première page"
      >
        Première page
      </a>
    </li>

    <li>
      <a
        class="fr-pagination__link fr-pagination__link--prev fr-pagination__link--lg-label"
        href={pagination.hasPrevious
          ? getPageLink(pagination.previousPage)
          : undefined}
        aria-disabled={!pagination.hasPrevious ? true : undefined}
        title="Page précédente"
      >
        Page précédente
      </a>
    </li>

    {#if pagination.hasFirstPageLandmark}
      <li>
        <a
          class="fr-pagination__link"
          title="Page {pagination.firstPage}"
          href={getPageLink(pagination.firstPage)}
        >
          {pagination.firstPage}
        </a>
      </li>
    {/if}

    {#if pagination.hasLeftTruncature}
      <li data-testid="left-truncature">
        <span class="fr-pagination__link fr-unhidden-lg"> ... </span>
      </li>
    {/if}

    {#each pagination.windowPages as page}
      <li>
        <a
          class="fr-pagination__link"
          class:fr-unhidden-lg={page > pagination.firstPage &&
            page != currentPage &&
            page < pagination.lastPage}
          title="Page {page}"
          aria-current={page === currentPage ? "page" : undefined}
          href={page === currentPage ? undefined : getPageLink(page)}
        >
          {page}
        </a>
      </li>
    {/each}

    {#if pagination.hasRightTruncature}
      <li data-testid="right-truncature">
        <span class="fr-pagination__link fr-unhidden-lg"> ... </span>
      </li>
    {/if}

    {#if pagination.hasLastPageLandmark}
      <li>
        <a
          class="fr-pagination__link"
          title="Page {pagination.lastPage}"
          href={getPageLink(pagination.lastPage)}
        >
          {pagination.lastPage}
        </a>
      </li>
    {/if}

    <li>
      <a
        class="fr-pagination__link fr-pagination__link--next fr-pagination__link--lg-label"
        href={pagination.hasNext ? getPageLink(pagination.nextPage) : undefined}
        aria-disabled={!pagination.hasNext ? true : undefined}
        title="Page suivante"
      >
        Page suivante
      </a>
    </li>

    <li>
      <a
        class="fr-pagination__link fr-pagination__link--last"
        href={pagination.hasNext ? getPageLink(pagination.lastPage) : undefined}
        aria-disabled={!pagination.hasNext ? true : undefined}
        title="Dernière page"
      >
        Dernière page
      </a>
    </li>
  </ul>
</nav>
