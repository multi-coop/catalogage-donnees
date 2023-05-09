<script lang="ts">
  import type { Tag as TagType } from "src/definitions/tag";
  import { transformTagToSelectOption } from "src/lib/transformers/form";
  import { createEventDispatcher } from "svelte";
  import Select from "../Select/Select.svelte";
  import Tag from "../Tag/Tag.svelte";

  export let tags: TagType[];
  export let name: string;
  export let id: string = name;
  export let error = "";
  export let selectedTags: TagType[] = [];

  let value: string | null = null;

  const dispatch = createEventDispatcher<{ change: TagType[] }>();

  const handleChange = () => {
    const tagId = value;
    value = null; // Auto-reset HTML select.

    const tagHasBeenAlreadySelected = selectedTags.find(
      (tag) => tag.id === tagId
    );
    if (tagHasBeenAlreadySelected) return;

    const tag = tags.find((item) => item.id === tagId);
    if (!tag) return;

    selectedTags = [...selectedTags, tag];

    dispatch("change", selectedTags);
  };

  const handleSelectTag = (e: CustomEvent<TagType>) => {
    selectedTags = selectedTags.filter((item) => item.id !== e.detail.id);
    dispatch("change", selectedTags);
  };
</script>

<Select
  {error}
  bind:value
  on:change={handleChange}
  required
  label={"Mots-clés"}
  hintText="Les mots-clés seront utilisés par les réutilisateurs pour affiner leur recherche. Sélectionnez ceux qui vous semblent les plus représentatifs de vos données."
  {id}
  {name}
  placeholder="Ajouter un mot-clé"
  options={tags.map(transformTagToSelectOption)}
/>

<div role="list">
  {#each selectedTags as { id, name }}
    <Tag role={"listitem"} on:click={handleSelectTag} {name} {id} />
  {/each}
</div>

<style>
  div[role="list"] {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
  }
</style>
