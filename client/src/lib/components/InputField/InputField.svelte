<script lang="ts">
  import type { TrustedHtml } from "src/lib/util/html";
  import TextOrHtml from "../TextOrHtml/TextOrHtml.svelte";
  import RequiredMarker from "../RequiredMarker/RequiredMarker.svelte";

  // If support for other input types is added, add it here.
  type SupportedInputType = "text" | "date" | "email";

  export let name: string;
  export let label: string;
  export let hintText: string | TrustedHtml = "";
  export let type: SupportedInputType = "text";
  export let required = false;
  export let value: string | null;
  export let error = "";

  $: id = name;
  $: hintTextId = `${name}-desc-hint`;
  $: errorId = `${name}-desc-error`;
</script>

<div class="fr-input-group fr-mb-4w" class:fr-input-group--error={error}>
  <label class="fr-label" for={id}>
    {label}
    {#if required}
      <RequiredMarker />
    {/if}
    {#if hintText}
      <span class="fr-hint-text" id={hintTextId}>
        <TextOrHtml value={hintText} />
      </span>
    {/if}
  </label>

  {#if type === "date"}
    <div class="fr-input-wrap">
      <input
        class="fr-input"
        class:fr-input--error={error}
        aria-describedby={error ? errorId : undefined}
        {id}
        {name}
        {type}
        {required}
        {value}
        on:input
        on:blur
      />
    </div>
  {:else}
    <input
      class="fr-input"
      class:fr-input--error={error}
      aria-describedby={error ? errorId : undefined}
      {id}
      {name}
      {type}
      {required}
      {value}
      on:input
      on:blur
    />
  {/if}

  {#if error}
    <p id={errorId} class="fr-error-text">
      {error}
    </p>
  {/if}
</div>

<style>
  /* Fix a parsing issue. Sometimes when a markdown string is parsed into html the result string is wrapped by a <p> tag */
  span > p {
    font-size: inherit;
  }
</style>
