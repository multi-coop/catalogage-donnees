<script lang="ts">
  import { onMount } from "svelte";
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
</script>

<svelte:head>
  <link rel="apple-touch-icon" href={appleTouchFavicon} />
  <!-- 180×180 -->
  <link rel="icon" href={svgFavicon} type="image/svg+xml" />
  <link rel="shortcut icon" href={icoFavicon} type="image/x-icon" />
  <!-- 32×32 -->
  <link rel="manifest" href={manifest} crossorigin="use-credentials" />
</svelte:head>

<slot />
