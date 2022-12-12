<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { escape } from "$lib/util/string";
  import { clickOutside } from "$lib/actions/clickOutside";

  export let value = "";
  export let error = "";
  export let suggestions: string[] = [];

  let showSuggestions = false;

  const dispatch = createEventDispatcher<{ input: string }>();

  $: filteredSuggestions = suggestions.filter((item) =>
    item.match(new RegExp(escape(value), "i"))
  );

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
  <label class="fr-label" for="license">
    Licence de réutilisation
    <span class="fr-hint-text" id="license-desc-hint">
      Indiquez la <a
        href="https://www.data.gouv.fr/fr/pages/legal/licences"
        target="_blank"
        rel="noreferrer"
        title="Voir les licences de réutilisation sur data.gouv.fr"
      >
        licence de réutilisation
      </a> associée au jeu de données.
    </span>
  </label>

  <input
    class="fr-input"
    class:fr-input--error={error}
    type="text"
    id="license"
    name="license"
    bind:value
    role="combobox"
    autocomplete="off"
    aria-controls="license-results"
    aria-autocomplete="list"
    aria-expanded={showSuggestions}
    aria-describedby={error ? "license-desc-error" : null}
    on:input={onInput}
    on:focus={() => (showSuggestions = true)}
  />

  <ul
    id="license-results"
    class="fr-raw-list dropdown--list"
    role="listbox"
    aria-label="Licences"
  >
    {#if showSuggestions}
      {#each filteredSuggestions as item}
        <li
          id="license-{item}"
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
    {/if}
  </ul>

  {#if error}
    <p id="license-desc-error" class="fr-error-text">
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
