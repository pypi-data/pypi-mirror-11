# -*- coding: UTF-8 -*-
logger.info("Loading 1 objects to table system_siteconfig...")
# fields: id, default_build_method, next_partner_id, site_company, system_note_type, default_event_type, site_calendar, max_auto_events, clients_account, sales_vat_account, sales_account, suppliers_account, purchases_vat_account, purchases_account, wages_account, clearings_account
loader.save(create_system_siteconfig(1,None,233,None,None,None,1,72,None,None,None,None,None,None,None,None))

loader.flush_deferred_objects()
