<script lang="ts">
  import type { SelectOption } from "src/definitions/form";
  import RequiredMarker from "../RequiredMarker/RequiredMarker.svelte";
  import { escape } from "src/lib/util/string";

  export let value: string | null = null;
  export let name: string;
  export let error = "";

  let currentLiIndex = 0;

  let suggestionList: HTMLElement;
  let previousNode: HTMLElement;

  $: regexp = value ? new RegExp(escape(value), "i") : null;
  $: filteredSuggestions = showSuggestions
    ? suggestions.filter((item) => (regexp ? item.label.match(regexp) : true))
    : [];

  export let suggestions: SelectOption<number>[] = [
    {
      label: "tata",
      value: 1,
    },
    {
      label: "toto",
      value: 2,
    },
    {
      label: "titi",
      value: 3,
    },
  ];

  let setSelectedOption = (value: string): SelectOption<number> | undefined => {
    return suggestions.find((item) => item.label === value);
  };
  let showSuggestions = false;

  const handleInput = (ev: Event & { currentTarget: HTMLInputElement }) => {
    value = ev.currentTarget.value;
  };

  const handleKeyboard = (e: KeyboardEvent) => {
    let suggestionItems = suggestionList.childNodes;

    console.log("BEFORE:", {
      currentLiIndex,
      itemLenght: suggestionItems.length,
    });

    switch (e.key) {
      case "Enter":
        showSuggestions = !showSuggestions;

        break;

      case "Escape":
        showSuggestions = false;
        break;

      case "ArrowDown":
        currentLiIndex = currentLiIndex + 1;
        if (currentLiIndex === suggestionItems.length) {
          currentLiIndex = 0;
        }
        break;

      case "ArrowUp":
        if (currentLiIndex === 0) {
          currentLiIndex = suggestionItems.length - 1;
        } else {
          currentLiIndex = currentLiIndex - 1;
        }

      default:
        break;
    }
  };
</script>

<div
  class="fr-input-group dropdown fr-my-4w"
  class:fr-input-group--error={error}
>
  <label class="fr-label" for={name}>
    Format(s) des données
    <RequiredMarker />
    <span class="fr-hint-text" id="select-hint-dataformats-hint">
      Sélectionnez ici les différents formats de données qu'un réutilisateur
      potentiel pourrait exploiter.
    </span>
  </label>

  <input
    on:keydown={handleKeyboard}
    class="fr-input"
    class:fr-input--error={error}
    type="text"
    name="geographicalCoverage"
    id={name}
    {value}
    required
    role="combobox"
    autocomplete="off"
    aria-controls={`${name}-suggestions`}
    aria-autocomplete="list"
    aria-expanded={showSuggestions}
    aria-describedby={error ? "geographicalCoverage-desc-error" : null}
    on:input={handleInput}
    on:focus={() => (showSuggestions = true)}
    on:focusout={() => (showSuggestions = false)}
  />

  <ul
    bind:this={suggestionList}
    class:hide={!showSuggestions}
    id={`${name}-suggestions`}
    role="listbox"
    aria-label="Formats de données"
  >
    {#each filteredSuggestions as { label, value }, index}
      <li
        class:focused={index === currentLiIndex}
        id={value.toString()}
        role="option"
      >
        {label}
      </li>
    {/each}
  </ul>
</div>

<style>
  .hide {
    display: none;
  }

  .focused {
    background-color: bisque;
  }
</style>
