<script lang="ts">
  import { page } from "$app/stores";
  import Footer from "src/lib/components/Footer/Footer.svelte";
  import Header from "src/lib/components/Header/Header.svelte";
  import Page404Template from "src/lib/templates/Page404Template/Page404Template.svelte";
  import Page500Template from "src/lib/templates/Page500Template/Page500Template.svelte";
</script>

<Header />

<section class="fr-container fr-mt-9w">
  {#if $page.status === 404}
    <Page404Template />
  {/if}

  {#if $page.status >= 500}
    <Page500Template />
  {/if}
</section>

<Footer />

<style>
  section {
    margin-bottom: 8rem;
  }
</style>
