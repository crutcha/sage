# Eidetic

# Lab/Testing
Vagrant is used to handle dynamic provision/teardown of lab environment used for testing. See [this documentation here](https://github.com/crutcha/eidetic/tree/master/vagrant) to get setup.

# Todo

- [ ] Update README with project info
- [x] Dockerize development setup
- [ ] Dockerize deployment setup
- [x] Get basic Celery/Flask integration working 
- [ ] Design how "Provider" objects for specific devices will work (L2/Switch, L3/Router, etc...)
- [ ] Create celery tasks to scrape providers by type and merge data into Neo4j
- [ ] Basic admin UI to add both devices/providers
- [ ] Vagrant file setup for virtual lab to use for testing. (vQFX, vMX, vSRX, ASA, NX-OS)