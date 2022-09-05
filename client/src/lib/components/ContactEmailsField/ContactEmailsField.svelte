<script lang="ts">
  import RequiredMarker from "../RequiredMarker/RequiredMarker.svelte";

  export let contactEmails: string[] = [""];
  export let errors: string[] = [];

  $: hasAtLeastOneEmail = contactEmails.some((email) => !!email);

  const add = () => {
    contactEmails = contactEmails.concat("");
    errors = errors.concat("");
  };

  const remove = (i: number) => {
    contactEmails = contactEmails.filter((_, itemIndex) => {
      return i !== itemIndex;
    });

    errors = errors.filter((_, itemIndex) => {
      return i !== itemIndex;
    });

    if (contactEmails.length === 0) {
      add();
    }
  };
</script>

<fieldset class="fr-fieldset fr-my-4w" aria-labelledby="contactEmails-legend">
  <legend
    class="fr-fieldset__legend fr-text--regular"
    id="contactEmails-legend"
  >
    E-mail(s) personnel(s)
    <RequiredMarker />
    <span class="fr-hint-text" id="contactEmails-desc-hint">
      Au moins une adresse e-mail est demandée. Ces emails seront régulièrement
      vérifiés afin d'assurer la bonne maintenabilité des jeux de données.
    </span>
  </legend>

  <ul class="fr-fieldset__content fr-raw-list fr-mb-3w">
    {#each contactEmails as _, i}
      <li>
        <div class="contact-entry">
          <label for="contactEmails-{i}" hidden>Contact {i}</label>
          <input
            class="fr-input fr-mr-1w"
            class:fr-input--error={errors[i]}
            aria-describedby={errors[i]
              ? `contactEmails-${i}-desc-error`
              : null}
            type="email"
            id="contactEmails-{i}"
            data-testid="contactEmails"
            placeholder="Adresse e-mail"
            name="contactEmails-{i}"
            required={!hasAtLeastOneEmail}
            on:change
            on:blur
            bind:value={contactEmails[i]}
          />
          <button
            type="button"
            class="fr-btn fr-btn--secondary fr-icon-delete-fill"
            title="Supprimer cet e-mail de contact"
            on:click|preventDefault={() => remove(i)}
          />
        </div>

        {#if errors[i]}
          <p id="contactEmails-{i}-desc-error" class="fr-error-text">
            {errors[i]}
          </p>
        {/if}
      </li>
    {/each}
  </ul>

  <button
    type="button"
    class="fr-btn fr-btn--secondary fr-icon-edit-fill fr-btn--icon-left contact-entry-add"
    on:click|preventDefault={() => add()}
  >
    Ajouter un contact
  </button>
</fieldset>

<style>
  .contact-entry {
    display: flex;
    margin: 8px 0;
  }
</style>
