<script lang="ts">
  import type { SelectOption } from "src/definitions/form";
  import RequiredMarker from "../RequiredMarker/RequiredMarker.svelte";
  import { escape } from "src/lib/util/string";

  export let name: string;
  export let error = "";

  let suggestionList: HTMLElement;

  let value: string | null = null;
  let currentLiIndex: number = 0;
  let showSuggestions = false;
  let selectedOption: SelectOption<number> | undefined;

  let textBoxHasFocus = false;

  $: console.log({ value, showSuggestions, textBoxHasFocus, currentLiIndex });

  $: regexp = value ? new RegExp(escape(value), "i") : null;

  $: filteredSuggestions = showSuggestions
    ? suggestions.filter((item) => (regexp ? item.label.match(regexp) : true))
    : [];

  $: activeSuggestionDescendant = currentLiIndex
    ? `suggestion-item-${currentLiIndex}`
    : null;

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
    {
      label: "fruiti",
      value: 4,
    },
    {
      label: "tarte",
      value: 5,
    },
  ];

  let setSelectedOption = (value: string): SelectOption<number> | undefined => {
    return filteredSuggestions.find((item) => item.label === value.trim());
  };

  const handleClickOption = (optionValue: string) => {
    selectedOption = setSelectedOption(optionValue);

    if (selectedOption) {
      value = selectedOption.label;
    }
    showSuggestions = false;
  };

  const handleInput = (ev: Event & { currentTarget: HTMLInputElement }) => {
    value = ev.currentTarget.value;
  };

  const manageKeyboardInterractions = (e: KeyboardEvent) => {
    let suggestionItems = suggestionList.childNodes;

    if (e.altKey && e.key === "ArrowDown") {
      // Opens the listbox without moving focus or changing selection.
      showSuggestions = true;
      textBoxHasFocus = false;
      return;
    }

    // Manage keyboard interracions when textbox has focus
    if (textBoxHasFocus) {
      switch (e.key) {
        case "Enter":
          //  Closes the listbox if it is displayed.

          if (showSuggestions) {
            textBoxHasFocus = false;
            showSuggestions = false;
          }

          break;

        case "Escape":
          //If the listbox is displayed, closes it.

          if (showSuggestions) {
            textBoxHasFocus = true;
            showSuggestions = false;
            return;
          }

          // if the listbox is not displayed, clears the textbox.

          if (!showSuggestions) {
            textBoxHasFocus = true;
            value = "";
          }
          break;

        case "ArrowDown":
          // If the textbox is not empty and the listbox is displayed, moves visual focus to the first suggested value.
          textBoxHasFocus = false;

          if (value && showSuggestions) {
            currentLiIndex = 0;
          }

          // the textbox is empty and the listbox is not displayed, opens the listbox and moves visual focus to the first option.

          if (!value && !showSuggestions) {
            currentLiIndex = 0;
            showSuggestions = true;
          }

          break;

        case "ArrowUp":
          // console.log("tata");
          // if the textbox is not empty and the listbox is displayed, moves visual focus to the last suggested value.

          if (!value && showSuggestions) {
            currentLiIndex = filteredSuggestions.length;
          }

          // If the textbox is empty, first opens the listbox if it is not already displayed and then moves visual focus to the last option.

          if (!value && !showSuggestions) {
            textBoxHasFocus = false;
            showSuggestions = true;
            currentLiIndex = suggestions.length - 1;
          }

        default:
          break;
      }

      return;
    }
    // Manage keyboard interracions when listbox has focus

    if (!textBoxHasFocus) {
      switch (e.key) {
        case "Enter":
          /**
         * 
          Sets the textbox value to the content of the focused option in the listbox.
          Closes the listbox.
          Sets visual focus on the textbox.

        */
          if (!currentLiIndex) {
            return;
          }
          const selectedSuggestionItem =
            suggestionItems[currentLiIndex].textContent;

          if (showSuggestions && selectedSuggestionItem) {
            selectedOption = setSelectedOption(selectedSuggestionItem);

            if (selectedOption) {
              value = selectedOption.label;
              showSuggestions = false;
            }
          }

          textBoxHasFocus = true;
          break;

        case "Escape":
          /**
         * 

            Closes the listbox.
            Sets visual focus on the textbox.

        */

          showSuggestions = false;
          textBoxHasFocus = true;
          break;

        /**
           * 
              Moves visual focus to the next option.
              If visual focus is on the last option, moves visual focus to the first option.
              Note: This wrapping behavior is useful when Home and End move the editing cursor as described below.

          */

        case "ArrowDown":
          currentLiIndex += 1;

          if (currentLiIndex === suggestionItems.length) {
            currentLiIndex = 0;
          }
          break;

        case "ArrowUp":
          /**
           * 
              Moves visual focus to the previous option.
              If visual focus is on the first option, moves visual focus to the last option.
              Note: This wrapping behavior is useful when Home and End move the editing cursor as described below.

          */
          if (currentLiIndex === 0) {
            currentLiIndex = suggestionItems.length - 1;
          } else {
            currentLiIndex -= 1;
          }
          break;
        case "ArrowRight":
          /**
           * 
            Moves visual focus to the textbox and moves the editing cursor one character to the right.

          */
          textBoxHasFocus = true;
          break;
        case "ArrowLeft":
          /**
           *  	Moves visual focus to the textbox and moves the editing cursor one character to the left.
           */
          textBoxHasFocus = true;
        default:
          break;
      }
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
    on:keydown={manageKeyboardInterractions}
    class="fr-input"
    class:fr-input--error={error}
    class:inputOutline={textBoxHasFocus}
    type="text"
    {name}
    id={name}
    {value}
    required
    role="combobox"
    autocomplete="off"
    aria-controls={`${name}-suggestions`}
    aria-autocomplete="list"
    aria-expanded={showSuggestions}
    aria-describedby={error ? "geographicalCoverage-desc-error" : null}
    aria-activedescendant={activeSuggestionDescendant}
    on:input={handleInput}
    on:focus={() => (textBoxHasFocus = true)}
    on:focusout={() => (textBoxHasFocus = false)}
  />

  <ul
    bind:this={suggestionList}
    class:hide={!showSuggestions}
    id={`${name}-suggestions`}
    role="listbox"
    aria-label="Formats de données"
    class:focused={!textBoxHasFocus}
  >
    {#each filteredSuggestions as { label }, index}
      <li
        class:focused={index === currentLiIndex}
        id={`suggestion-item-${index}`}
        role="option"
        aria-label={name}
        aria-selected={index === currentLiIndex}
        on:click={() => handleClickOption(label)}
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
    border: 1px solid saddlebrown;
  }

  input:focus-visible {
    /* Remove the focus visible default behavior. Will be managed programatticaly  */
    outline-style: none;
  }

  .inputOutline {
    outline-style: solid !important;
  }
</style>
