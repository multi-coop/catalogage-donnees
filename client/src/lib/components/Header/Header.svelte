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
              <p class="fr-logo">
                République
                <br />Française
              </p>
            </div>

            {#if Maybe.Some($account)}
              <div class="fr-header__navbar">
                <button
                  class="fr-btn--menu fr-btn"
                  data-fr-opened="false"
                  aria-controls="modal-menu"
                  aria-haspopup="menu"
                  title="Menu"
                  id="fr-btn-menu-mobile"
                >
                  Menu
                </button>
              </div>
            {/if}
          </div>
          <div class="fr-header__service">
            <a href={paths.home} title="Accueil - {SITE_TITLE}">
              <p class="fr-header__service-title">{SITE_TITLE}</p>
              <p
                class="fr-badge fr-badge--success fr-badge--sm fr-badge--no-icon"
              >
                Bêta
              </p>
            </a>
          </div>
        </div>
        <div class="fr-header__tools tools-container">
          <div class="fr-header__tools-links">
            {#if Maybe.Some($account)}
              <p>
                {$account.email}
              </p>
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
            {/if}
          </div>
        </div>
      </div>
    </div>
  </div>
  <div
    class="fr-header__menu fr-modal"
    id="modal-menu"
    data-fr-js-modal="true"
    data-fr-js-header-modal="true"
    aria-labelledby="fr-btn-menu-mobile"
  >
    <div class="fr-container">
      <button
        class="fr-btn fr-btn--close"
        aria-controls="modal-menu"
        data-fr-js-modal-button="true">Fermer</button
      >

      <div class="fr-header__menu-links" />

      {#if Maybe.Some($account)}
        <nav
          class="fr-nav"
          role="navigation"
          aria-label="Menu principal"
          id="header-navigation"
          data-fr-js-navigation="true"
        >
          <ul class="fr-nav__list">
            {#each $navigationItems as { label, href }}
              <li class="fr-nav__item" data-fr-js-navigaton-item="true">
                <a
                  {href}
                  class="fr-nav__link"
                  aria-current={href === path ? "page" : undefined}
                >
                  {label}
                </a>
              </li>
            {/each}
          </ul>
        </nav>
      {/if}
    </div>
  </div>
</header>

<style>
  a {
    display: flex;
    gap: 15px;
  }

  @media (max-width: 1440px) and (min-width: 768px) {
    /* To give a bit space between the beta banner and the tools (login/out button, email adress) only for LG and MD screen */
    .tools-container {
      padding-right: 80px;
    }
  }
</style>
