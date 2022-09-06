<script lang="ts">
  import { goto } from "$app/navigation";

  import { page } from "$app/stores";

  import padlock from "$lib/assets/padlock.svg";
  import type { Organization } from "src/definitions/organization";
  import Spinner from "src/lib/components/Spinner/Spinner.svelte";
  import {
    createDatapassUser,
    getDatapassUserInfoFromURLSearchParams,
  } from "src/lib/repositories/datapass";
  import { login } from "src/lib/stores/auth";
  import { onMount } from "svelte";

  let hasError = false;
  let loading = true;
  let email: string;
  let token: string | null;
  let organizations: Organization[] = [];

  let errorWhenCreatingDatapassUser: boolean;
  let pickedOrganization: Organization;

  onMount(async () => {
    const params = $page.url.searchParams;

    try {
      const { token: opaqueToken, info } =
        getDatapassUserInfoFromURLSearchParams(params);

      organizations = info.organizations;

      if (organizations.length === 0) {
        hasError = true;
        return;
      }
      email = info.email;
      token = opaqueToken;
    } catch (error) {
      hasError = true;
    } finally {
      loading = false;
    }
  });

  const handleSubmitForm = async () => {
    const siret = pickedOrganization.siret;

    if (!siret || !email || !token) {
      return;
    }

    loading = true;

    try {
      const { account, apiToken } = await createDatapassUser({
        fetch,
        token,
        data: { siret, email },
      });

      login(account, apiToken);

      await goto("/");
    } catch (error) {
      errorWhenCreatingDatapassUser = true;
    } finally {
      loading = false;
    }
  };
</script>

{#if loading}
  <div class="spinner-container">
    <Spinner />
  </div>
{:else}
  <section class="fr-container fr-py-8w">
    <div class="fr-grid-row">
      <div class="fr-col-12 container">
        <div class="padlock-container fr-mr-3w">
          <img class="padlock" alt="" src={padlock} />
        </div>

        {#if hasError}
          <div>
            <h3>Nous n'arrivons pas à retrouver vos informations ...</h3>

            <p>
              En raison d'un problème technique, nous sommes actuellement dans
              l'incapacité de retrouver les informations des organisations
              auxquelles vous êtes rattachés.
              <br />
              Veuillez-nous en excuser.
            </p>
          </div>
        {:else if errorWhenCreatingDatapassUser}
          <div>
            <h3>Nous n'arrivons pas à créer votre compte...</h3>

            <p>
              En raison d'un problème technique, nous sommes actuellement dans
              l'incapacité de créer votre compte
              <br />
              Veuillez-nous en excuser.
            </p>
          </div>
        {:else}
          <div>
            <h3>Votre compte peut être associé à plusieurs organisations.</h3>

            <p>
              A l’heure actuelle nous ne supportons qu’une seule organisation
              par compte.
            </p>

            <form on:submit|preventDefault={handleSubmitForm}>
              <div class="fr-form-group">
                <fieldset class="fr-fieldset">
                  <legend
                    class="fr-fieldset__legend fr-text--regular"
                    id="radio-legend"
                  >
                    Veuillez sélectionner l’organisation à laquelle vous
                    souhaitez être associé :
                  </legend>
                  <div class="fr-fieldset__content">
                    {#each organizations as organization}
                      <div class="fr-radio-group">
                        <input
                          bind:group={pickedOrganization}
                          type="radio"
                          id={organization.siret}
                          name="organization"
                          value={organization}
                        />
                        <label class="fr-label" for={organization.siret}
                          >{organization.name}</label
                        >
                      </div>
                    {/each}
                  </div>
                </fieldset>
              </div>

              <button
                disabled={!pickedOrganization}
                type="submit"
                class="fr-btn fr-btn--icon-right  fr-icon-git-pull-request-line"
                >Associer mon compte</button
              >
            </form>
          </div>
        {/if}
      </div>
    </div>
  </section>
{/if}

<style>
  .spinner-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 200px;
  }
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
