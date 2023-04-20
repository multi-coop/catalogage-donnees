<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let value = "";

  const dispatch = createEventDispatcher<{ submit: string }>();

  const onSubmit = () => dispatch("submit", value);
</script>

<form
  class="fr-search-bar fr-search-bar--lg"
  role="search"
  on:submit|preventDefault={onSubmit}
>
  <label for="q" class="fr-label">Rechercher</label>
  <input
    id="q"
    type="search"
    class="fr-input"
    name="q"
    bind:value
    placeholder="Ex : taux de contamination COVID, nombre de naissances en France, ..."
  />
  <button type="submit" class="fr-btn"> Rechercher </button>
</form>
