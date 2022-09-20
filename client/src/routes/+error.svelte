<script lang="ts">
  import { page } from "$app/stores";
</script>

<section class="fr-container fr-mt-9w">
  <h1>
    {$page.status}: {$page.error ? $page.error.message : "unknown error"}
  </h1>
</section>
