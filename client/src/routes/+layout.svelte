<script lang="ts">
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import {
    pageTitle,
    siteDescription,
    siteTitle,
  } from "$lib/stores/layout/title";

  // CSS
  import "../app.css";
  import "../styles/dsfr-icon-extras.css";

  // DSFR Assets
  import appleTouchFavicon from "@gouvfr/dsfr/dist/favicon/apple-touch-icon.png";
  import svgFavicon from "@gouvfr/dsfr/dist/favicon/favicon.svg";
  import icoFavicon from "@gouvfr/dsfr/dist/favicon/favicon.ico";
  import manifest from "@gouvfr/dsfr/dist/favicon/manifest.webmanifest";

  onMount(async () => {
    // Load the DSFR asynchronously, and only on the browser (not in SSR).
    await import("@gouvfr/dsfr/dist/dsfr/dsfr.module.min.js");
  });

  $: title = $pageTitle;
</script>

<svelte:head>
  <link rel="apple-touch-icon" href={appleTouchFavicon} />
  <!-- 180×180 -->
  <link rel="icon" href={svgFavicon} type="image/svg+xml" />
  <link rel="shortcut icon" href={icoFavicon} type="image/x-icon" />
  <!-- 32×32 -->
  <link rel="manifest" href={manifest} crossorigin="use-credentials" />

  <title>{$pageTitle}</title>

  <!-- Meta tags for Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:title" content={title} />
  <meta name="description" content={siteDescription} />
  <meta property="og:description" content={siteDescription} />
  <meta
    property="og:image"
    content="https://systeme-de-design.gouv.fr/src/img/systeme-de-design.gouv.fr.jpg"
  />
  <meta property="og:image:alt" content="République Française - {siteTitle}" />
  <meta property="og:url" content={$page.url.toString()} />

  <!-- Meta tags for Twitter -->
  <meta name="twitter:card" content="summary" />
</svelte:head>

<slot />
