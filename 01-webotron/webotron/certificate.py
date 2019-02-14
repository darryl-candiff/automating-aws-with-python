# -*- coding: utf-8 -*-

"""Classes for AWS Certificate Manager."""

class CertificateManager:
    """Manage AWS Certificates"""

    def __init__(self, session):
        """Create an AWS CertificateManager instance."""
        self.session = session
        self.client = self.session.client('acm', region_name='us-east-1')

    def cert_matches(self, cert_arn, domain_name):
        """Check is domain matches cert"""
        cert_details = self.client.describe_certificate(CertificateArn=cert_arn)
        alt_names = cert_details['Certificate']['SubjectAlternativeNames']
        for name in alt_names:
            if name == domain_name:
                return True
            if name[0] == '*' and domain_name.endswith(name[1:]):
                return True
        return False

    def find_matching_cert(self, domain_name):
        """Return certifications for domain name"""
        paginator = self.client.get_paginator('list_certificates')
        for page in paginator.paginate(CertificateStatuses=['ISSUED']):
           for cert in page['CertificateSummaryList'] :
               if self.cert_matches(cert['CertificateArn'], domain_name):
                   return cert

        return None
