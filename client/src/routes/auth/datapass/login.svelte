<script lang="ts">
  import { goto } from "$app/navigation";

  import { page } from "$app/stores";
  import type { User, UserRole } from "src/definitions/auth";
  import Spinner from "src/lib/components/Spinner/Spinner.svelte";
  import { login } from "src/lib/stores/auth";
  import { onMount } from "svelte";
  import padlock from "$lib/assets/padlock.svg";

  let loading = true;
  let hasError = false;

  onMount(async () => {
    const params = $page.url.searchParams;

    const role = params.get("role");
    const token = params.get("api_token");
    const email = params.get("email");

    if (!email || !token || !role) {
      hasError = true;
      loading = false;
      return;
    }

    const user: User = {
      role: role as UserRole,
      apiToken: token,
      email,
    };

    login(user);

    await goto("/");

    loading = false;
  });
</script>

{#if loading}
  <div class="spinner-container">
    <Spinner />
  </div>
{/if}

{#if hasError}
  <section class="fr-container fr-py-8w">
    <div class="fr-grid-row">
      <div class="fr-col-12 container">
        <div class="padlock-container fr-mr-3w">
          <img class="padlock" alt="" src={padlock} />
        </div>

        <div>
          <h3>Un problème est survenu lors de la connexion</h3>

          <p>
            Nous ne pouvons vous connecter au site actuellement. Merci de
            contacter l'administrateur du site
          </p>
        </div>
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
</style>
