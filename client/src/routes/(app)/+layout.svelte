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
  <div class="fr-skiplinks">
    <nav class="fr-container" role="navigation" aria-label="Accès rapide">
      <ul class="fr-skiplinks__list">
        <li>
          <a class="fr-nav__link" href="#contenu">Contenu</a>
        </li>
        <li>
          <a class="fr-nav__link" href="#header-navigation">Menu</a>
        </li>
        <li>
          <a class="fr-nav__link" href="#footer">Pied de page</a>
        </li>
      </ul>
    </nav>
  </div>

  <Header />

  <main id="contenu" class="fr-mb-8w">
    <slot />
  </main>

  <Footer />
</LayoutProviders>
