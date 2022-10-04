<script lang="ts">
  import { goto } from "$app/navigation";

  import books from "$lib/assets/books-circle.svg";
  import { USER_DOCUMENTATION_LINK } from "src/constants";
  import MonCompteProButton from "src/lib/components/MonCompteProButton/MonCompteProButton.svelte";
  import { getApiUrl } from "src/lib/fetch";

  const triggerDataPassLoginFlow = async () => {
    await goto(`${getApiUrl()}/auth/datapass/login/`);
  };
</script>

<section class="banner fr-py-8w">
  <div class="fr-container">
    <div class="fr-grid-row">
      <div class="fr-col-12 title-container">
        <img class="books-image" alt="" src={books} />

        <div class="fr-pl-3w">
          <h1>Bienvenue sur le service de catalogage de données de l’État</h1>
          <p>
            Ce service permet aux administrations centrales et aux opérateurs
            sous leur tutelle de créer, gérer et ouvrir leurs catalogues de
            données dans le cadre notamment de <a
              href="https://www.etalab.gouv.fr/politique-de-la-donnee-des-algorithmes-et-des-codes-sources-15-strategies-ministerielles-et-500-actions-pour-accelerer/"
              >leur stratégie en matière de politique de la donnée</a
            >.
          </p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="fr-container fr-py-8w">
  <div class="fr-grid-row">
    <div class="fr-col-12">
      <h3>Connexion à catalogue.data.gouv.fr</h3>
      <div class="button-container">
        <MonCompteProButton on:click={triggerDataPassLoginFlow} />
      </div>
      <p>
        Pour en savoir plus, vous pouvez consulter <a
          class="fr-link"
          target="_blank"
          href={USER_DOCUMENTATION_LINK}>la documentation détaillée</a
        >.
      </p>
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

  .title-container,
  .button-container {
    display: flex;
  }

  .title-container {
    align-items: center;
    gap: 15px;
  }
</style>
