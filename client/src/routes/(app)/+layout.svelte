<script lang="ts">
  import Header from "$lib/components/Header/Header.svelte";
  import Footer from "$lib/components/Footer/Footer.svelte";
  import { onMount } from "svelte";
  import LayoutProviders from "$lib/providers/LayoutProviders.svelte";
  import { account, apiToken, refresh } from "$lib/stores/auth";
  import { Maybe } from "$lib/util/maybe";
  import { getMe } from "$lib/repositories/auth";

  onMount(async () => {
    if (Maybe.Some($account)) {
      // Ensure user session is still valid and has updated info.
      Maybe.map(await getMe({ fetch, apiToken: $apiToken }), (freshAccount) =>
        refresh(freshAccount)
      );
    }
  });
</script>

<LayoutProviders>
  <Header account={$account} />

  <main id="contenu" class="fr-mb-8w">
    <slot />
  </main>

  <Footer />
</LayoutProviders>
