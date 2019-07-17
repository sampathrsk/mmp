from django import forms
REGIONS= [
    ('','--------'),
    ('us-east-1', 'US East(N. Virginia)'),
    ('us-east-2', 'US East(Ohio)'),
    ('us-west-1', 'US West(N. California)'),
    ('us-west-2', 'US West(Oregon)'),
    ('ca-central-1', 'Canada(Central)'),
    ('eu-west-1', 'EU(Ireland)'),
    ('eu-central-1', 'EU(Frankfurt)'),
    ('eu-west-2', 'EU(London)'),
    ('ap-southeast-1', 'Asia Pacific(Singapore)'),
    ('ap-southeast-2', 'Asia Pacific(Sydney)'),
    ('ap-northeast-2', 'Asia Pacific(Seoul)'),
    ('ap-northeast-1', 'Asia Pacific(Tokyo)'),
    ('ap-south-1', 'Asia Pacific(Mumbai)'),
    ('sa-east-1', 'South America(Sao Paulo)'),
    ]
ITYPE=[('t2.nano', 't2.nano'),
        ('t2.micro', 't2.micro'),
        ('t2.small', 't2.small'),
        ('t2.medium', 't2.medium'),
        ]
VERSIONS=[('17.04','zesty-17.04'),
          ('16.04 LTS','xenial-16.04 LTS'),
          ('14.04 LTS','trusty-14.04 LTS'),
          ('12.04 LTS','precise-12.04 LTS'),
          ('17.10','artful-17.10'),]
class awsform(forms.Form):
     region = forms.CharField(widget=forms.Select(choices=REGIONS))
     vpc = forms.CharField(widget=forms.Select())
     launch_config = forms.CharField(widget=forms.Select())
     itypeM = forms.CharField(widget=forms.Select(choices=ITYPE))
     itypeS = forms.CharField(widget=forms.Select(choices=ITYPE))
     version = forms.CharField(widget=forms.Select(choices=VERSIONS))

