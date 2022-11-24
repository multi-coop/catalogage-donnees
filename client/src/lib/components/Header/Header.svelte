<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { logout, account } from "$lib/stores/auth";
  import { navigationItems } from "$lib/stores/layout/navigation";
  import { SITE_TITLE } from "src/constants";
  import paths from "$lib/paths";
  import { Maybe } from "$lib/util/maybe";

  $: path = $page.url.pathname;

  const onClickLogout = async () => {
    logout();
    await goto("/");
  };
</script>

<header role="banner" class="fr-header">
  <div class="fr-header__body">
    <div class="fr-container">
      <div class="fr-header__body-row">
        <div class="fr-header__brand fr-enlarge-link">
          <div class="fr-header__brand-top">
            <div class="fr-header__logo">
              <a href="/" aria-label="Accueil - Etalab">
                <p class="fr-logo">
                  République
                  <br />Française
                </p>
              </a>
            </div>

            {#if Maybe.Some($account)}
              <div class="fr-header__navbar">
                <button
                  class="fr-btn--menu fr-btn"
                  data-fr-opened="false"
                  aria-controls="modal-491"
                  aria-haspopup="menu"
                  id="button-492"
                  title="Menu"
                >
                  Menu
                </button>
              </div>
            {/if}
          </div>

          <div class="fr-header__service">
            <a href="/" title={`Accueil - ${SITE_TITLE}- Etalab`}>
              <p class="fr-header__service-title">{SITE_TITLE}</p>
            </a>
          </div>
        </div>

        {#if Maybe.Some($account)}
          <div class="fr-header__tools">
            <div class="fr-header__tools-links">
              <ul class="fr-btns-group">
                <li>
                  <button
                    class="fr-btn fr-btn--icon-left fr-icon-logout-box-r-line"
                    on:click={onClickLogout}
                  >
                    Déconnexion
                  </button>
                </li>
              </ul>
            </div>
          </div>
        {/if}
      </div>
    </div>
  </div>
  <div
    class="fr-header__menu fr-modal"
    id="modal-491"
    aria-labelledby="button-492"
  >
    {#if Maybe.Some($account)}
      <div class="fr-container">
        <button
          class="fr-btn--close fr-btn"
          aria-controls="modal-491"
          title="Fermer"
        >
          Fermer
        </button>

        <div class="fr-header__menu-links" />
        <nav
          class="fr-nav"
          id="navigation-494"
          role="navigation"
          aria-label="Menu principal"
        >
          <ul class="fr-nav__list">
            {#each $navigationItems as { label, href }}
              <li data-fr-js-navigaton-item="true">
                <a
                  aria-current={href === path ? "page" : undefined}
                  class="fr-nav__link"
                  {href}
                  target="_self">{label}</a
                >
              </li>
            {/each}
          </ul>
        </nav>
      </div>
    {/if}
  </div>
</header>
