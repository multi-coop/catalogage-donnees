<script lang="ts">
  import { slugify } from "src/lib/util/format";
  export let buttonPlaceholder: string;
  export let buttonText = buttonPlaceholder;
  export let label: string;
  export let isOverlayOpen = false;

  $: slug = slugify(label);
</script>

<div class="container">
  <span data-testId={`${slug}-label`} id={`${slug}`}>{label}</span>
  <button
    aria-labelledby={`${slug}-label`}
    class="fr-select"
    data-testId={`${slug}-button`}
    on:click>{buttonText}</button
  >

  {#if isOverlayOpen}
    <div class="overlay">
      <slot />
    </div>
  {/if}
</div>

<style>
  button {
    text-align: left;
  }
  .container {
    position: relative;
    box-sizing: border-box;
    width: 100%;
  }
  .overlay {
    padding: 10px;
    background-color: var(--grey-1000-75);
    box-shadow: 0 0 10px var(--grey-925);
    z-index: 10;
    max-height: 32vh;
    width: 100%;
    overflow-x: hidden;
    overflow-y: scroll;
    position: absolute;
    border: 1px solid var(--background-contrast-grey);
  }
</style>
