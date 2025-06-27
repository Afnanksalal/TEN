import { library, config } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  faHome,
  faBriefcase,
  faCommentDots,
  faDollarSign,
  faFileAlt,
  faChartLine,
  faSatelliteDish,
  faGavel,
  faDoorOpen,
  faBars,
  faTimes,
  faBullhorn, // ADD THIS
  faUsers // ADD THIS
} from '@fortawesome/free-solid-svg-icons'

config.autoAddCss = false

library.add(
  faHome,
  faBriefcase,
  faCommentDots,
  faDollarSign,
  faFileAlt,
  faChartLine,
  faSatelliteDish,
  faGavel,
  faDoorOpen,
  faBars,
  faTimes,
  faBullhorn, // ADD THIS
  faUsers // ADD THIS
)

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.component('font-awesome-icon', FontAwesomeIcon)
})