<script>
  import padlock from "$lib/assets/padlock.svg";
</script>

<section class="fr-container fr-py-8w">
  <div class="fr-grid-row">
    <div class="fr-col-12 container">
      <div class="padlock-container fr-mr-3w">
        <img class="padlock" alt="" src={padlock} />
      </div>

      <div>
        <h3>Votre compte n’est associé à aucune organisation enregistrée...</h3>

        <p>
          Vous ne pouvez pas accéder au service pour le moment, mais vous pouvez
          effectuer une demande d’enregistrement afin d’intégrer votre
          organisation à notre outil.
        </p>
      </div>
    </div>
  </div>
</section>

<style>
  .padlock {
    width: 108px;
    height: 124px;
  }

  .padlock-container {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .container {
    display: flex;
  }
</style>
