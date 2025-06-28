import { library, config } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { 
  faHome, 
  faBriefcase, // <-- Added for Risk Assessment
  faCommentDots, 
  faDollarSign, 
  faFileAlt, 
  faBullseye,   // <-- ADD THIS LINE for Competitor Radar
  faChartLine, 
  faGavel, 
  faDoorOpen, 
  faBullhorn, 
  faUsers,
  faArrowRight,
  faStar,
  faBars,
  faCompass
} from '@fortawesome/free-solid-svg-icons'

// This is important, we are going to let Nuxt worry about the CSS
config.autoAddCss = false

// You can add your icons directly in this plugin. See https://fontawesome.com/v5/
library.add(
  faHome,
  faBriefcase,
  faCommentDots,
  faDollarSign,
  faFileAlt,
  faBullseye, // <-- ADD THIS LINE HERE TOO
  faChartLine,
  faGavel,
  faDoorOpen,
  faBullhorn,
  faUsers,
  faArrowRight,
  faStar,
  faBars,
  faCompass
)

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.component('font-awesome-icon', FontAwesomeIcon, {})
})