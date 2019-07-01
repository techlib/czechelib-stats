<i18n src="../locales/common.yaml"></i18n>

<template>
    <v-app>
        <!--LoginDialog v-if="!$store.getters.loggedIn"></LoginDialog-->
        <template>
            <SidePanel />

            <v-toolbar app clipped-left>
                <!--v-toolbar-side-icon></v-toolbar-side-icon-->
                <v-toolbar-title>CzechELib stats</v-toolbar-title>

                <v-divider
                        class="mx-3"
                        inset
                        vertical
                ></v-divider>

                <div class="org">
                    <span class="sc">{{ $t('organization') }}</span>: <strong>{{ selectedOrganization.name }}</strong>
                </div>

                <v-spacer></v-spacer>
                <v-toolbar-items class="hidden-sm-and-down">
                    <v-select
                            v-model="appLang"
                            :items="['cs','en']"
                            prepend-icon="fa-globe"
                            class="short"
                    >
                    </v-select>
                    <v-divider
                            class="mx-3"
                            inset
                            vertical
                    ></v-divider>
                    <v-avatar size="36px" color="primary" class="mt-2">
                        <v-tooltip bottom>
                            <template v-slot:activator="{ on }">
                            <span v-on="on" >
                                <img
                                        v-if="$store.getters.avatarImg"
                                        src="https://avatars0.githubusercontent.com/u/9064066?v=4&s=460"
                                        alt="Avatar"
                                >
                                <span v-else-if="$store.getters.loggedIn" class="white--text headline">{{ $store.getters.avatarText }}</span>
                                <v-icon
                                        v-else
                                        dark
                                >fa-user</v-icon>
                            </span>
                            </template>

                            <span>{{ $store.getters.usernameText }}</span>
                        </v-tooltip>
                    </v-avatar>
                </v-toolbar-items>

            </v-toolbar>

            <v-content>
                <v-container fluid>

                    <router-view/>

                    <v-snackbar v-model="snackbarShow">
                        {{ snackbarText }}
                        <v-btn dark flat @click="hideSnackbar">
                            Close
                        </v-btn>
                    </v-snackbar>
                </v-container>
            </v-content>
        </template>
    </v-app>
</template>

<script>
  import SidePanel from './SidePanel'
  //import LoginDialog from '../components/LoginDialog'
  import {mapState, mapActions} from 'vuex'

  export default {
    name: 'Dashboard',
    components: {
      SidePanel,
      //LoginDialog
    },
    data () {
      return {
        navbarExpanded: false,
        appLang: 'cs',
      }
    },
    computed: {
      ...mapState({
        selectedOrganization: 'selectedOrganization',
        snackbarText: state => state.snackbarContent,
      }),
      snackbarShow: {
        get () {
          return this.$store.state.snackbarShow
        },
        set (newValue) {
          if (newValue === false)
            this.hideSnackbar()
        }
      },
    },
    methods: {
      ...mapActions({
        hideSnackbar: 'hideSnackbar',
        start: 'start',
      }),
      toggleNavbar () {
        this.navbarExpanded = !this.navbarExpanded
      },
    },
    created () {
      this.start()
    },
    watch: {
      appLang () {
        this.$i18n.locale = this.appLang
      }
    }

  }
</script>

<style lang="scss">

    div.org {
        display: inline-block;
        font-size: 1.25rem;
    }

    .sc {
        font-variant: small-caps;
    }

    .v-select.v-text-field.short input {
        max-width: 0;
    }

    section.header {
        margin-bottom: 2rem;
    }

    div.fields {
        margin-top: 1rem;
    }

</style>