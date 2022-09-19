<script lang="ts">
  import type { ExtraField, ExtraFieldValue } from "src/definitions/catalogs";
  import { Maybe } from "src/lib/util/maybe";

  export let extraFields: ExtraField[];
  export let extraFieldValues: ExtraFieldValue[];

  const makeItems = (fields: ExtraField[], values: ExtraFieldValue[]) => {
    return fields.map(({ id, title }) => {
      const value = values.find(({ extraFieldId }) => id === extraFieldId);
      return {
        id,
        label: title,
        value: Maybe.map(value, ({ value }) => value),
      };
    });
  };

  $: items = makeItems(extraFields, extraFieldValues);
</script>

<div class="fr-grid-row fr-grid-row--gutters">
  {#each items as { id, label, value } (id)}
    <div class="fr-col-12 fr-col-sm-6">
      <div class="fr-text--sm fr-my-0 fr-text-mention--grey">
        {label}
      </div>
      <div>
        {#if Maybe.Some(value)}
          {value}
        {:else}
          -
        {/if}
      </div>
    </div>
  {/each}
</div>
