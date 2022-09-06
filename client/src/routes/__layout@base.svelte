<script lang="ts">
  import Header from "$lib/components/Header/Header.svelte";
  import Footer from "$lib/components/Footer/Footer.svelte";
  import { onMount } from "svelte";
  import LayoutProviders from "$lib/providers/LayoutProviders.svelte";
  import { account, apiToken } from "$lib/stores/auth";
  import { checkLogin } from "$lib/repositories/auth";
  import { Maybe } from "$lib/util/maybe";

  onMount(async () => {
    if (Maybe.Some($account)) {
      // Ensure user session is still valid.
      await checkLogin({ fetch, apiToken: $apiToken });
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
