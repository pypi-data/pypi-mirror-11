# Copyright 2014 Facebook, Inc.

# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.

# As with any software that integrates with the Facebook platform, your use
# of this software is subject to the Facebook Developer Principles and
# Policies [http://developers.facebook.com/policy/]. This copyright notice
# shall be included in all copies or substantial portions of the software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from __future__ import print_function
from __future__ import unicode_literals

import time
import os
import sys
from facebookads.objects import *
from facebookads.api import *
from facebookads.exceptions import *

this_dir = os.path.dirname(__file__)
repo_dir = os.path.join(this_dir, os.pardir, os.pardir)
sys.path.insert(1, repo_dir)

config_file = open(os.path.join(this_dir, 'config.json'))
config = json.load(config_file)
config_file.close()

ad_account_id = config['account_id']
access_token = config['access_token']
app_id = config['app_id']
app_secret = config['app_secret']
page_id = config['page_id']
connections_id = page_id

FacebookAdsApi.init(app_id, app_secret, access_token)


homepage_campaign = AdCampaign(parent_id=ad_account_id)
homepage_campaign.update({
    AdCampaign.Field.name: 'Homepage Ads',
    AdCampaign.Field.buying_type: AdCampaign.BuyingType.fixed_cpm,
    AdCampaign.Field.objective: AdCampaign.Objective.none,
})
homepage_campaign.remote_create()

campaign_group_id = homepage_campaign.get_id()

# _DOC open [ADSET_CREATE_HOMEPAGE]
# _DOC vars [ad_account_id:s, campaign_group_id]
from facebookads.objects import AdAccount, AdSet
ad_account = AdAccount(ad_account_id)
rate_cards = ad_account.get_rate_cards()
country = rate_cards[0][RateCard.Field.country]
rate = rate_cards[0][RateCard.Field.rate]

impressions = 5000
lifetime_budget = str(rate * 5000)
end_date = int(time.time() + 12 * 3600)

ad_set = AdSet(parent_id=ad_account_id)
ad_set.update({
    AdSet.Field.name: 'Adset Homepage Ads',
    AdSet.Field.campaign_group_id: campaign_group_id,
    AdSet.Field.lifetime_budget: lifetime_budget,
    AdSet.Field.lifetime_imps: impressions,
    AdSet.Field.bid_type: AdSet.BidType.multi_premium,
    AdSet.Field.bid_info: {
        AdSet.Field.BidInfo.clicks: 20,
        AdSet.Field.BidInfo.social: 40,
        AdSet.Field.BidInfo.impressions: 40
    },
    AdSet.Field.targeting: {
        TargetingSpecsField.page_types: ['home'],
        TargetingSpecsField.geo_locations: {
            'countries': [country],
        }
    },
    AdSet.Field.end_time: end_date,
})

ad_set.remote_create()
print(ad_set)
# _DOC close [ADSET_CREATE_HOMEPAGE]

ad_set.remote_delete()
homepage_campaign.remote_delete()

campaign = AdCampaign(parent_id=ad_account_id)
campaign.update({
    AdCampaign.Field.name: 'My Campaign',
    AdCampaign.Field.objective: AdCampaign.Objective.none,
})
campaign.remote_create()

campaign_group_id = campaign.get_id()

# _DOC open [ADSET_CREATE]
# _DOC vars [ad_account_id:s, campaign_group_id]
from facebookads.objects import AdSet, TargetingSpecsField

adset = AdSet(parent_id=ad_account_id)
adset.update({
    AdSet.Field.name: 'My Ad Set',
    AdSet.Field.campaign_group_id: campaign_group_id,
    AdSet.Field.daily_budget: 1000,
    AdSet.Field.bid_type: AdSet.BidType.absolute_ocpm,
    AdSet.Field.bid_info: {
        AdSet.Field.BidInfo.actions: 150,
    },
    AdSet.Field.targeting: {
        TargetingSpecsField.geo_locations: {
            'countries': ['US'],
        },
    },
    AdSet.Field.status: AdSet.Status.paused,
})

adset.remote_create()
print(adset)
# _DOC close [ADSET_CREATE]
adset.remote_delete()

connections_id = page_id
# _DOC open [ADSET_CREATE_APP_CONNECTIONS_TARGETING]
# _DOC vars [ad_account_id:s, campaign_group_id, connections_id]
from facebookads.objects import AdSet

ad_set = AdSet(parent_id=ad_account_id)
ad_set.update({
    AdSet.Field.name: 'Android Connections Targeting - Ad Set',
    AdSet.Field.campaign_group_id: campaign_group_id,
    AdSet.Field.bid_type: AdSet.BidType.cpc,
    AdSet.Field.bid_info: {
        AdSet.Field.BidInfo.clicks: 150,
    },
    AdSet.Field.daily_budget: 2000,
    AdSet.Field.targeting: {
        TargetingSpecsField.geo_locations: {
            'countries': ['US'],
        },
        TargetingSpecsField.connections: [connections_id],
        TargetingSpecsField.user_os: ['Android'],
    },
    AdSet.Field.status: AdSet.Status.paused,
})

ad_set.remote_create()
print(ad_set)
# _DOC close [ADSET_CREATE_APP_CONNECTIONS_TARGETING]

# _DOC open [ADSET_GET_ADGROUPS]
# _DOC vars [ad_set_id]
from facebookads.objects import AdSet, AdGroup

ad_set = AdSet(ad_set_id)
ad_group_iter = ad_set.get_ad_groups(fields=[AdGroup.Field.name])
for ad_group in ad_group_iter:
    print ad_group[AdGroup.Field.name]
# _DOC close [ADSET_GET_ADGROUPS]

campaign = AdCampaign(parent_id=ad_account_id)
campaign.update({
    AdCampaign.Field.name: 'My Page Likes Campaign',
    AdCampaign.Field.objective: AdCampaign.Objective.page_likes,
})
campaign.remote_create()

campaign_group_id = campaign.get_id()

# _DOC open [ADSET_CREATE_CPC_PROMOTING_PAGE]
# _DOC vars [ad_account_id:s, page_id:s, campaign_group_id:s]
import time
from facebookads.objects import AdSet

adset = AdSet(parent_id=ad_account_id)
adset[AdSet.Field.name] = 'My Ad Set'
adset[AdSet.Field.status] = AdSet.Status.paused
adset[AdSet.Field.daily_budget] = 10000
adset[AdSet.Field.bid_type] = AdSet.BidType.cpc
adset[AdSet.Field.bid_info] = {
    'CLICKS': 150,
}
adset[AdSet.Field.promoted_object] = {'page_id': page_id}
adset[AdSet.Field.targeting] = {
    'geo_locations': {
        'countries': ['US'],
    }
}
adset[AdSet.Field.start_time] = int(time.time())
adset[AdSet.Field.campaign_group_id] = campaign_group_id
adset.remote_create()

print(adset)
# _DOC close [ADSET_CREATE_CPC_PROMOTING_PAGE]
adset.remote_delete()
campaign.remote_delete()

ad_set_id = ad_set.get_id()
# _DOC open [ADSET_READ_ADCREATIVE]
# _DOC vars [ad_set_id]
adset = AdSet(fbid=ad_set_id)
adset.get_ad_creatives([AdCreative.Field.object_story_id])
# _DOC close [ADSET_READ_ADCREATIVE]

ad_set.remote_delete()
campaign.remote_delete()
