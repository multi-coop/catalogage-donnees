<script lang="ts">
  export let controlId: string;
</script>

<dialog
  aria-labelledby="fr-modal-title-modal-1"
  id={controlId}
  class="fr-modal"
>
  <div class="fr-container fr-container--fluid fr-container-md">
    <div class="fr-grid-row fr-grid-row--center">
      <div class="fr-col-12 fr-col-md-8 fr-col-lg-6">
        <div class="fr-modal__body">
          <div class="fr-modal__header">
            <button class="fr-btn--close fr-btn" aria-controls={controlId}
              >Fermer</button
            >
          </div>
          <div class="fr-modal__content">
            <slot name="modal-content" />
          </div>

          <slot name="modal-footer" />
        </div>
      </div>
    </div>
  </div>
</dialog>
