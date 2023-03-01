<script lang="ts">
  import type { SelectOption } from "src/definitions/form";
  import RequiredMarker from "../RequiredMarker/RequiredMarker.svelte";
  import { escape } from "src/lib/util/string";
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher<{
    selectOption: SelectOption<number | string | null>;
    addItem: string;
  }>();

  export let name: string;
  export let label = "";
  export let hintText = "";
  export let options: SelectOption<number | string | null>[];
  export let error = "";
  export let value = "";
  export let labelledby = "";

  let suggestionList: HTMLElement;
  let currentLiIndex = 0;
  let showSuggestions = false;
  let selectedOption: SelectOption<number | string | null>;
  let textBoxHasFocus = false;

  $: regexp = value ? new RegExp(escape(value), "i") : null;

  $: filteredSuggestions = showSuggestions
    ? options.filter((item) => (regexp ? item.label.match(regexp) : true))
    : [];

  const getSelectedOption = (
    value: string
  ): SelectOption<number | string | null> | undefined =>
    filteredSuggestions.find((item) => item.label === value.trim());

  const handleSelectOption = (option: SelectOption<number | string | null>) => {
    selectedOption = option;
    dispatch("selectOption", selectedOption);
    showSuggestions = false;
  };

  const handleClickOption = (optionValue: string) => {
    const foundOption = getSelectedOption(optionValue);

    if (foundOption) {
      value = foundOption.label;
      handleSelectOption(foundOption);
    }
    showSuggestions = false;
  };

  const handleInput = (ev: Event & { currentTarget: HTMLInputElement }) => {
    textBoxHasFocus = true;
    showSuggestions = true;
    value = ev.currentTarget.value;
  };

  const handeChange = (ev: Event & { currentTarget: HTMLInputElement }) => {
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

          e.preventDefault();

          if (showSuggestions) {
            textBoxHasFocus = false;
            showSuggestions = false;
          }

          if (value) {
            const selectedOption = getSelectedOption(value);

            if (selectedOption) {
              handleSelectOption(selectedOption);
            }
          }

          break;

        case "Escape":
          // if the listbox is not displayed, clears the textbox.

          if (!showSuggestions) {
            textBoxHasFocus = true;
            value = "";
            return;
          }
          //If the listbox is displayed, closes it.

          if (showSuggestions) {
            textBoxHasFocus = true;
            showSuggestions = false;
            return;
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
            currentLiIndex = options.length - 1;
          }

          break;

        default:
          break;
      }

      return;
    }
    // Manage keyboard interracions when listbox has focus

    if (!textBoxHasFocus) {
      switch (e.key) {
        case "Enter": {
          /**
           * 
            Sets the textbox value to the content of the focused option in the listbox.
            Closes the listbox.
            Sets visual focus on the textbox.
  
          */

          e.preventDefault();

          const selectedSuggestionItem =
            suggestionItems[currentLiIndex].textContent;

          if (showSuggestions && selectedSuggestionItem) {
            const foundOption = getSelectedOption(selectedSuggestionItem);

            if (foundOption) {
              value = foundOption.label;
              showSuggestions = false;
              handleSelectOption(foundOption);
            }
          }

          textBoxHasFocus = true;
          break;
        }

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
          break;
        default:
          break;
      }
    }
  };

  const handleFocusIn = () => {
    showSuggestions = true;
    textBoxHasFocus = false;
  };
</script>

<div class="fr-input-group dropdown" class:fr-input-group--error={error}>
  {#if label}
    <label class="fr-label" for={name}>
      {label}
      <RequiredMarker />
      {#if hintText}
        <span class="fr-hint-text" id={`select-hint-${name}-hint`}>
          {hintText}
        </span>
      {/if}
    </label>
  {/if}

  <div class="input-container">
    <input
      on:change={handeChange}
      on:keydown={manageKeyboardInterractions}
      class="fr-input"
      class:fr-input--error={error}
      class:inputOutline={textBoxHasFocus}
      type="text"
      {name}
      {value}
      required
      role="combobox"
      autocomplete="off"
      aria-controls={`${name}-suggestions`}
      aria-labelledby={!label ? labelledby : null}
      aria-autocomplete="list"
      aria-expanded={showSuggestions}
      aria-describedby={error ? `${name}-desc-error` : null}
      aria-activedescendant={showSuggestions
        ? `suggestion-item-${currentLiIndex}`
        : null}
      on:input={handleInput}
      on:focus={handleFocusIn}
      on:focusout
    />

    <slot name="add-item" />
  </div>

  <ul
    bind:this={suggestionList}
    class:hide={!showSuggestions}
    class="fr-raw-list dropdown--list"
    id={`${name}-suggestions`}
    role="listbox"
    aria-label="Formats de données"
    class:suggestionlist--focused={!textBoxHasFocus}
  >
    {#each filteredSuggestions as { label }, index}
      <li
        class:focused={index === currentLiIndex}
        class="dropdown--list-item"
        id={`suggestion-item-${index}`}
        role="option"
        aria-label={name}
        aria-selected={index === currentLiIndex}
        on:mousedown={() => handleClickOption(label)}
      >
        {label}
      </li>
    {/each}
  </ul>

  {#if error}
    <p id="{name}-desc-error" class="fr-error-text">
      {error}
    </p>
  {/if}
</div>

<style>
  .hide {
    display: none;
  }

  .suggestionlist--focused {
    outline: solid;
    outline-offset: 2px;
    outline-width: 2px;
    outline-color: #0a76f6;
  }

  .focused {
    background-color: var(--background-default-grey-hover);
  }

  input:focus-visible {
    /* Remove the focus visible default behavior. Will be managed programatticaly  */
    outline-style: none;
  }

  .inputOutline {
    outline-style: solid !important;
  }

  .dropdown--list {
    width: 100%;
    height: 100%;
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

  .input-container {
    gap: 15px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>
