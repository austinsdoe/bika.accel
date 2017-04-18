from DateTime import DateTime
from Products.Archetypes.config import REFERENCE_CATALOG
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from bika.lims import bikaMessageFactory as _
from bika.lims.utils import t
from bika.lims import logger
from bika.lims.subscribers import skip
from bika.lims.subscribers import doActionFor
import App
import transaction
import urllib
import urlparse

def get_patient(ar):
    return ar.Schema().getField('Patient').get(ar) \
        if 'Patient' in ar.Schema() else None

def get_doctor(ar):
    return ar.Schema().getField('Doctor').get(ar) \
        if 'Doctor' in ar.Schema() else None

def get_recipients(ar):
    recips = []

    bs = ar.bika_setup
    sch = bs.Schema()
    bs_allowdist = sch['AllowResultsDistributionToPatients'].get(bs)
    bs_pubprefs = sch['PatientPublicationPreferences'].get(bs)

    # Add Patient recipients
    pat = get_patient(ar)
    if pat:
        sch = pat.Schema()
        pa_allowdist_field = pat.getField('AllowResultsDistribution')
        inherit_field = pat.getField('DefaultResultsDistribution')
        mobile = pat.getMobilePhone() if pat.getMobilePhone() else None
        pa_allowdist = pa_allowdist_field.get(pat) if pa_allowdist_field else False
        inherit = inherit_field.get(pat) if inherit_field else True
        if inherit == True:
            # Gets the results distribution from the client
            client = ar.aq_parent
            inherit_field = client.getField('DefaultResultsDistributionToPatients')
            cl_allowdist_field = client.getField('AllowResultsDistributionToPatients')
            cl_allowdist = cl_allowdist_field.get(client) if cl_allowdist_field else False
            inherit = inherit_field.get(client) if inherit_field else True

            if inherit == True and bs_allowdist == True:
                # Gets the results distribution from BikaSetup
                recips.append({'title':pat.Title(),
                               'mobile':mobile,
                               'pubpref':bs_pubprefs})

            elif inherit == False and cl_allowdist == True:
                # Gets the results distribution from Client
                cl_pubpref_field = client.getField('PatientPublicationPreferences')
                cl_pubpref = cl_pubpref_field.get(client) if cl_pubpref_field else []
                recips.append({'title':pat.Title(),
                               'mobile':mobile,
                               'pubpref':cl_pubpref})

        elif pa_allowdist == True:
            # Gets the pub preferences from the patient
            pub_field = pat.getField('PublicationPreferences')
            pubpref = pub_field.get(pat) if pub_field else []
            recips.append({'title':pat.Title(),
                           'mobile':mobile,
                           'pubpref':pubpref})

    # Add Doctor recipient
    doctor = get_doctor(ar)
    if doctor:
        mobile = pat.getMobilePhone() if pat.getMobilePhone() else None
        pubpref = doctor.getField('PublicationPreference')
        pubpref = pubpref.get(doctor) if pubpref else []
        recips.append({'title':doctor.Title(),
                       'mobile':mobile,
                       'pubpref':pubpref})

    return recips

#return a SMS message for publication of result
#details = (<CName>,<AS title>,<CSID>,<Result and Unit>,<AR URL>,
# <lab email address>,<lab telephone #>,<Lab name>)
def getSMSResultString(result_details):
    return ("Dear %s, the %s result for Sample %s is "
    "%s. More information at %s. Please direct queries "
    "to %s, tel %s. Regards, %s.") % tuple(result_details)

#return a SMS message for publication of notification
#details = (<PName>,<AS title>,<CSID>,<Client name>,<Lab name>)
def getSMSNotifyString(notify_details):
    return ("Dear %s, the %s result for Sample %s is available. Please "
    "visit your care provider %s for further "
    "information. Regards, %s.") % tuple(notify_details)

def smsSend(sms_number, sms_text):
    #Parameters
    registry = getUtility(IRegistry)
    port = str(registry.get('bika.accel.sms.port_number', '9000'))
    root = str(registry.get('bika.accel.sms.root_url', 'http://localhost'))
    send = str(registry.get('bika.accel.sms.send_url', 'send/sms/'))
    send += '/' if not send.endswith('/') else ''
    req_server = urlparse.urljoin(root+":"+port,send)
    req_param = urllib.quote(sms_number + '/' + sms_text)
    query_url = urlparse.urljoin(req_server, req_param)
    try: response = urllib.urlopen(query_url).read()
    except IOError as e:
        print "SMS API connection failure: " + query_url
        print(e)

def sms(instance, event):
    xstr = lambda s: '' if not s else str(s)
    # creation doesn't have a 'transition'
    if not event.transition:
        return

    # send sms when AR gets verified
    if event.transition.id in ['verify']:
        analyses = instance.getAnalyses(review_state='verified')
        recipients = get_recipients(instance)
        for recipient in recipients:
            sms_number = recipient['mobile']

            if 'smsNotify' in recipient['pubpref'] and sms_number:
                for analysisbrain in analyses:
                    analysis = analysisbrain.getObject()
                    csid = analysis.getClientSampleID()
                    sid = analysis.getSampleID()
                    notify_details = (recipient['title'],
                        analysis.getServiceTitle(),
                        csid if csid else sid,
                        analysis.getClient().getName(),
                        analysis.bika_setup.laboratory.Title())
                    sms_text = getSMSNotifyString(notify_details)
                    smsSend(sms_number, sms_text)

            if 'smsResult' in recipient['pubpref'] and sms_number:
                for analysisbrain in analyses:
                    analysis = analysisbrain.getObject()
                    csid = analysis.getClientSampleID()
                    sid = analysis.getSampleID()
                    result_details = (recipient['title'],
                        analysis.getServiceTitle(),
                        csid if csid else sid,
                        analysis.getResult() +
                        xstr(analysis.getService().getUnit()),
                        instance.absolute_url(),
                        analysis.bika_setup.laboratory.getEmailAddress(),
                        analysis.bika_setup.laboratory.getPhone(),
                        analysis.bika_setup.laboratory.Title())
                    sms_text = getSMSResultString(result_details)
                    smsSend(sms_number, sms_text)
