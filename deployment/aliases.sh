alias start_containers='docker-compose up -d'
alias stop_containers='docker-compose down'
alias pull_containers='docker-compose pull'
alias deploy_updates='bash deploy_updates.sh'
alias logs='docker-compose logs -f'

alias m='docker-compose run --rm www src/manage.py'
alias shell='m shell_plus --settings=streisand.settings.www_settings'
alias clean_slate='m reset_db --noinput && m migrate && m loaddata foundation'
alias fixtures='m loaddata dev'
