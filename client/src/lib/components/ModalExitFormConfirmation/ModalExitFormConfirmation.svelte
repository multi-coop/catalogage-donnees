<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import Modal from "../GenericModal/GenericModal.svelte";

  export let controlId: string;

  const dispatch = createEventDispatcher<{ confirm: void }>();
</script>

<Modal {controlId}>
  <div slot="modal-content">
    <h1 id="{controlId}-title" class="fr-modal__title">
      <span
        class="fr-icon-error-warning-fill fr-fi--md fr-text-default--error"
        aria-hidden="true"
      />
      Êtes-vous sûr de vouloir quitter ?
    </h1>
    <p>
      Il semblerait que vous ayez effectué des modifications non sauvegardées
      sur cette fiche de données. Souhaitez-vous vraiment quitter ce formulaire
      et perdre votre saisie ?
    </p>
  </div>

  <div slot="modal-footer" class="fr-modal__footer">
    <ul
      class="fr-btns-group fr-btns-group--right fr-btns-group--inline-reverse fr-btns-group--inline-lg fr-btns-group--icon-left"
    >
      <li>
        <button aria-controls={controlId} class="fr-btn fr-btn--secondary">
          Revenir au formulaire
        </button>

        <button on:click={() => dispatch("confirm")} class="fr-btn">
          Quitter sans sauvegarder
        </button>
      </li>
    </ul>
  </div>
</Modal>
