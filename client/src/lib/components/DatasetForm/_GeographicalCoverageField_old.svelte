<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { Maybe } from "$lib/util/maybe";
  import { escape } from "src/lib/util/string";
  import { clickOutside } from "$lib/actions/clickOutside";
  import RequiredMarker from "../RequiredMarker/RequiredMarker.svelte";

  export let value: string | null = null;
  export let error = "";
  export let suggestions: string[] = [];

  let showSuggestions = false;

  const dispatch = createEventDispatcher<{ input: string }>();

  $: regexp = Maybe.map(value, (v) => new RegExp(escape(v), "i"));
  $: filteredSuggestions = showSuggestions
    ? suggestions.filter((item) =>
        Maybe.Some(regexp) ? Maybe.Some(item.match(regexp)) : true
      )
    : [];

  const onInput = (ev: Event & { currentTarget: HTMLInputElement }) => {
    dispatch("input", ev.currentTarget.value);
  };

  const onSelectItem = (item: string) => {
    showSuggestions = false;
    dispatch("input", item);
  };
</script>

<div
  class="fr-input-group dropdown fr-my-4w"
  class:fr-input-group--error={error}
  use:clickOutside={{ callback: () => (showSuggestions = false) }}
>
  <label class="fr-label" for="geographicalCoverage">
    Couverture géographique
    <RequiredMarker />
    <span class="fr-hint-text" id="geographicalCoverage-desc-hint">
      Quelle est l'étendue de la zone couverte par ce jeu de données ?
    </span>
  </label>

  <input
    class="fr-input"
    class:fr-input--error={error}
    type="text"
    id="geographicalCoverage"
    name="geographicalCoverage"
    {value}
    required
    role="combobox"
    autocomplete="off"
    aria-controls="geographicalCoverage-results"
    aria-autocomplete="list"
    aria-expanded={showSuggestions}
    aria-describedby={error ? "geographicalCoverage-desc-error" : null}
    on:input={onInput}
    on:focus={() => (showSuggestions = true)}
  />

  <ul
    id="geographicalCoverage-results"
    class="fr-raw-list dropdown--list"
    role="listbox"
    aria-label="Suggestions"
  >
    {#each filteredSuggestions as item}
      <li
        id="geographicalCoverage-{item}"
        class="dropdown--list-item"
        role="option"
        tabindex="0"
        on:click={() => onSelectItem(item)}
        on:keydown={(ev) => {
          if (ev.key === "Enter") {
            onSelectItem(item);
          }
        }}
      >
        {item}
      </li>
    {/each}
  </ul>

  {#if error}
    <p id="geographicalCoverage-desc-error" class="fr-error-text">
      {error}
    </p>
  {/if}
</div>

<style>
  .dropdown {
    position: relative;
  }

  .dropdown--list {
    position: absolute;
    width: 100%;
    max-height: 32vh;
    overflow: scroll;
    background-color: var(--grey-1000-75);
    border: 1px solid var(--background-contrast-grey);
    box-shadow: 0 0 10px var(--grey-925);
    z-index: 10;
  }

  .dropdown--list-item {
    cursor: pointer;
    padding: 0.5rem 1rem;
    margin: 0;
    border-top: 1px solid var(--background-contrast-grey);
  }

  .dropdown--list-item:hover {
    background-color: var(--background-contrast-grey);
  }
</style>
