<script lang="ts">
  import type { SelectOption } from "src/definitions/form";
  import type { TrustedHtml } from "src/lib/util/html";
  import TextOrHtml from "../TextOrHtml/TextOrHtml.svelte";
  import RequiredMarker from "../RequiredMarker/RequiredMarker.svelte";

  export let label: string;
  export let id: string;
  export let name: string;
  export let options: SelectOption<string | TrustedHtml>[];

  export let placeholder = "";
  export let hintText: string | TrustedHtml = "";
  export let required = false;
  export let error = "";
  export let value: string | null = null;
</script>

<div class="fr-select-group" class:fr-select-group--error={error}>
  <label class="fr-label" for={id}>
    {label}
    {#if required}
      <RequiredMarker />
    {/if}

    {#if hintText}
      <span class="fr-hint-text" id="{name}-desc-hint">
        <TextOrHtml value={hintText} />
      </span>
    {/if}
  </label>
  <select
    aria-describedby={error ? `{name}-desc-error` : ""}
    class="fr-select"
    class:fr-select--error={error}
    {required}
    {id}
    {name}
    bind:value
    on:change
    on:blur
  >
    {#if placeholder}
      <option value={null} disabled>{placeholder}</option>
    {/if}

    {#each options as { value, label }}
      <option {value}>{label}</option>
    {/each}
  </select>

  {#if error}
    <p id="{name}-desc-error" class="fr-error-text">
      {error}
    </p>
  {/if}
</div>
