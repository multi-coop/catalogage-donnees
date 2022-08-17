<script>
  import books from "$lib/assets/books-circle.svg";
  import flowChart from "$lib/assets/registration_flow_chart.svg";
</script>

<section class="banner fr-py-8w">
  <div class="fr-container">
    <div class="fr-grid-row">
      <div class="fr-col-12 title-container">
        <img class="books-image" alt="" src={books} />

        <header class="fr-pl-3w">
          <h1>Bienvenue sur le service de catalogage de données de l’État</h1>
          <p>
            Ce service permet de favoriser la circulation des données entre les
            différentes administrations centrales et opérateurs de l’État.
            L’intégration des différentes organisations se fait progressivement
            et en fonction des demandes.
          </p>
        </header>
      </div>
    </div>
  </div>
</section>

<section class="fr-container fr-py-8w">
  <div class="fr-grid-row">
    <div class="fr-col-12">
      <h3>Comment accéder aux catalogues ?</h3>

      <p>
        L’accès aux catalogues s’effectue via le compte datapass. Il est pour
        l’instant possible uniquement aux agents des organisations enregistrées.
        Pour en savoir plus sur les moyens de s’enregistrer et intégrer son
        catalogue, vous pouvez consulter la documentation détaillée.
      </p>

      <div class="flow-chart-container fr-pt-5w">
        <img class="flow-chart" alt="" src={flowChart} />
      </div>
    </div>
  </div>
</section>

<style>
  .banner {
    background-color: var(--background-alt-blue-france);
  }

  .flow-chart {
    width: 414px;
    height: 428px;
  }

  .books-image {
    width: 215px;
    height: 215px;
  }

  .flow-chart-container {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .title-container {
    display: flex;
  }
</style>
