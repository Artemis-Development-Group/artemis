#!/usr/bin/env python
# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://code.reddit.com/LICENSE. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is artemis.
#
# The Original Developer is the Initial Developer.  The Initial Developer of
# the Original Code is artemis Inc.
#
# All portions of the code written by artemis are Copyright (c) 2006-2016 artemis
# Inc. All Rights Reserved.
###############################################################################


from r2.lib.utils.artemis_agent_parser import (
    AlienBlueDetector,
    BaconReaderDetector,
    detect,
    McArtemisDetector,
    NarwhalForArtemisDetector,
    ReaditDetector,
    ArtemisAndroidDetector,
    ArtemisIsFunDetector,
    ArtemisIOSDetector,
    ArtemisSyncDetector,
    RelayForArtemisDetector)
from r2.tests import ArtemisTestCase


class AgentDetectorTest(ArtemisTestCase):
    def test_artemis_is_fun_detector(self):
        user_agent = 'artemis is fun (Android) 4.1.15'
        agent_parsed = {}
        result = ArtemisIsFunDetector().detect(user_agent, agent_parsed)
        self.assertTrue(result)
        self.assertEqual(agent_parsed['browser']['name'], 'artemis is fun')
        self.assertEqual(agent_parsed['browser']['version'], '4.1.15')
        self.assertEqual(agent_parsed['platform']['name'], 'Android')
        self.assertEqual(agent_parsed['app_name'],
                         agent_parsed['browser']['name'])

    def test_artemis_android_detector(self):
        user_agent = 'ArtemisAndroid 1.1.5'
        agent_parsed = {}
        result = ArtemisAndroidDetector().detect(user_agent, agent_parsed)
        self.assertTrue(result)
        self.assertEqual(agent_parsed['browser']['name'],
                         ArtemisAndroidDetector.name)
        self.assertEqual(agent_parsed['browser']['version'], '1.1.5')
        self.assertTrue(agent_parsed['app_name'],
                        agent_parsed['browser']['name'])

    def test_artemis_ios_detector(self):
        user_agent = ('Artemis/Version 1.1/Build 1106/iOS Version 9.3.2 '
                      '(Build 13F69)')
        agent_parsed = {}
        result = ArtemisIOSDetector().detect(user_agent, agent_parsed)
        self.assertEqual(agent_parsed['browser']['name'],
                         ArtemisIOSDetector.name)
        self.assertEqual(agent_parsed['browser']['version'], '1.1')
        self.assertEqual(agent_parsed['platform']['name'], 'iOS')
        self.assertEqual(agent_parsed['platform']['version'], '9.3.2')
        self.assertEqual(agent_parsed['app_name'],
                         agent_parsed['browser']['name'])

    def test_alian_blue_detector(self):
        user_agent = 'AlienBlue/2.9.10.0.2 CFNetwork/758.4.3 Darwin/15.5.0'
        agent_parsed = {}
        result = AlienBlueDetector().detect(user_agent, agent_parsed)
        self.assertTrue(result)
        self.assertEqual(agent_parsed['browser']['name'],
                         AlienBlueDetector.name)
        self.assertEqual(agent_parsed['browser']['version'], '2.9.10.0.2')
        self.assertEqual(agent_parsed['app_name'],
                         agent_parsed['app_name'])

    def test_relay_for_artemis_detector(self):
        user_agent = 'Relay by /u/DBrady v7.9.32'
        agent_parsed = {}
        result = RelayForArtemisDetector().detect(user_agent, agent_parsed)
        self.assertTrue(result)
        self.assertEqual(agent_parsed['browser']['name'],
                         RelayForArtemisDetector.name)
        self.assertEqual(agent_parsed['browser']['version'], '7.9.32')
        self.assertEqual(agent_parsed['app_name'],
                         agent_parsed['browser']['name'])

    def test_artemis_sync_detector(self):
        user_agent = ('android:com.laurencedawson.artemis_sync:v11.4 '
                      '(by /u/ljdawson)')
        agent_parsed = {}
        result = ArtemisSyncDetector().detect(user_agent, agent_parsed)
        self.assertTrue(result)
        self.assertEqual(agent_parsed['browser']['name'],
                         ArtemisSyncDetector.name)
        self.assertEqual(agent_parsed['browser']['version'], '11.4')
        self.assertEqual(agent_parsed['app_name'],
                         agent_parsed['browser']['name'])

    def test_narwhal_detector(self):
        user_agent = 'narwhal-iOS/2306 by det0ur'
        agent_parsed = {}
        result = NarwhalForArtemisDetector().detect(user_agent, agent_parsed)
        self.assertTrue(result)
        self.assertEqual(agent_parsed['browser']['name'],
                         NarwhalForArtemisDetector.name)
        self.assertEqual(agent_parsed['platform']['name'], 'iOS')
        self.assertEqual(agent_parsed['app_name'],
                         agent_parsed['browser']['name'])

    def test_mcartemis_detector(self):
        user_agent = 'McArtemis - Artemis Client for iOS'
        agent_parsed = {}
        result = McArtemisDetector().detect(user_agent, agent_parsed)
        self.assertTrue(result)
        self.assertEqual(agent_parsed['browser']['name'],
                         McArtemisDetector.name)
        self.assertEqual(agent_parsed['platform']['name'], 'iOS')
        self.assertEqual(agent_parsed['app_name'],
                         agent_parsed['browser']['name'])

    def test_readit_detector(self):
        user_agent = (
            '(Readit for WP /u/MessageAcrossStudios) (Readit for WP '
            '/u/MessageAcrossStudios)')
        agent_parsed = {}
        result = ReaditDetector().detect(user_agent, agent_parsed)
        self.assertTrue(result)
        self.assertEqual(agent_parsed['browser']['name'], ReaditDetector.name)
        self.assertIsNone(agent_parsed.get('app_name'))

    def test_bacon_reader_detector(self):
        user_agent = 'BaconReader/3.0 (iPhone; iOS 9.3.2; Scale/2.00)'
        agent_parsed = {}
        result = BaconReaderDetector().detect(user_agent, agent_parsed)
        self.assertTrue(result)
        self.assertEqual(agent_parsed['browser']['name'],
                         BaconReaderDetector.name)
        self.assertEqual(agent_parsed['browser']['version'], '3.0')
        self.assertEqual(agent_parsed['platform']['name'], 'iOS')
        self.assertEqual(agent_parsed['platform']['version'], '9.3.2')
        self.assertEqual(agent_parsed['app_name'],
                         agent_parsed['browser']['name'])


class HAPIntegrationTests(ArtemisTestCase):
    """Tests to ensure that parsers don't confilct with existing onex."""
    # TODO (katie.atkinson): Add tests to ensure artemis parsers don't conflict
    # with httpagentparser detectors.
    def test_artemis_is_fun_integration(self):
        user_agent = 'artemis is fun (Android) 4.1.15'
        outs = detect(user_agent)
        self.assertEqual(outs['browser']['name'], 'artemis is fun')
        self.assertEqual(outs['dist']['name'], 'Android')

    def test_artemis_android_integration(self):
        user_agent = 'ArtemisAndroid 1.1.5'
        outs = detect(user_agent)
        self.assertEqual(outs['browser']['name'], 'Artemis: The Official App')
        self.assertEqual(outs['dist']['name'], 'Android')

    def test_artemis_ios_integration(self):
        user_agent = ('Artemis/Version 1.1/Build 1106/iOS Version 9.3.2 '
                      '(Build 13F69)')
        outs = detect(user_agent)
        self.assertEqual(outs['browser']['name'], ArtemisIOSDetector.name)

    def test_alien_blue_detector(self):
        user_agent = 'AlienBlue/2.9.10.0.2 CFNetwork/758.4.3 Darwin/15.5.0'
        outs = detect(user_agent)
        self.assertEqual(outs['browser']['name'], AlienBlueDetector.name)

    def test_relay_for_artemis_detector(self):
        user_agent = '  Relay by /u/DBrady v7.9.32'
        outs = detect(user_agent)
        self.assertEqual(outs['browser']['name'], RelayForArtemisDetector.name)

    def test_artemis_sync_detector(self):
        user_agent = ('android:com.laurencedawson.artemis_sync:v11.4 '
                      '(by /u/ljdawson)')
        outs = detect(user_agent)
        self.assertEqual(outs['browser']['name'], ArtemisSyncDetector.name)

    def test_narwhal_detector(self):
        user_agent = 'narwhal-iOS/2306 by det0ur'
        outs = detect(user_agent)
        self.assertEqual(outs['browser']['name'],
                         NarwhalForArtemisDetector.name)

    def test_mcartemis_detector(self):
        user_agent = 'McArtemis - Artemis Client for iOS'
        outs = detect(user_agent)
        self.assertEqual(outs['browser']['name'], McArtemisDetector.name)

    def test_readit_detector(self):
        user_agent = (
            '(Readit for WP /u/MessageAcrossStudios) '
            '(Readit for WP /u/MessageAcrossStudios)')
        outs = detect(user_agent)
        self.assertEqual(outs['browser']['name'], ReaditDetector.name)

    def test_bacon_reader_detector(self):
        user_agent = 'BaconReader/3.0 (iPhone; iOS 9.3.2; Scale/2.00)'
        outs = detect(user_agent)
        self.assertEqual(outs['browser']['name'], BaconReaderDetector.name)
