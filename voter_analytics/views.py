from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
import plotly.express as px
import plotly.io as pio
from django.utils.safestring import mark_safe

# Create your views here

# view for the list of voters
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    # the fields to display in the queryset for each voter to limit the data retrieved
    def get_queryset(self):
        queryset = Voter.objects.all()
        
        print(queryset.count())
        # get filters from request parameters
        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        elections = {
            'v20state': self.request.GET.get('v20state'),
            'v21town': self.request.GET.get('v21town'),
            'v21primary': self.request.GET.get('v21primary'),
            'v22general': self.request.GET.get('v22general'),
            'v23town': self.request.GET.get('v23town'),
        }

        # Apply filters
        if party_affiliation:
            queryset = queryset.filter(party_affiliation=party_affiliation)
        
        if min_dob:
            queryset = queryset.filter(date_of_birth__gte=min_dob)
        
        if max_dob:
            queryset = queryset.filter(date_of_birth__lte=max_dob)
        
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        
        for election_field, value in elections.items():
            if value == 'on':  # Checkbox fields will send 'on' if checked
                queryset = queryset.filter(**{election_field: True})
        
        print(f"Filtered voter count: {queryset.count()}")  # Debug: Check if records exist after filtering
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # additional context for the filter form
        context['party_affiliations'] = Voter._meta.get_field('party_affiliation').choices
        context['years'] = range(1900, 2024)  # range of years for date of birth filter
        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct().order_by('voter_score')
        
        return context
    

    
# gives the details of a specified voter
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'



# view for the graphs
class GraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        queryset = Voter.objects.all()

        # Retrieve filter parameters from request
        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        elections = {
            'v20state': self.request.GET.get('v20state'),
            'v21town': self.request.GET.get('v21town'),
            'v21primary': self.request.GET.get('v21primary'),
            'v22general': self.request.GET.get('v22general'),
            'v23town': self.request.GET.get('v23town'),
        }

        # Apply filters if present
        if party_affiliation:
            queryset = queryset.filter(party_affiliation=party_affiliation)
        
        if min_dob:
            queryset = queryset.filter(date_of_birth__gte=min_dob)
        
        if max_dob:
            queryset = queryset.filter(date_of_birth__lte=max_dob)
        
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        
        for election_field, value in elections.items():
            if value == 'on':  # Checkbox fields will send 'on' if checked
                queryset = queryset.filter(**{election_field: True})
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        # Graph 1: Histogram of Voters by Year of Birth
        birth_years = queryset.values_list('date_of_birth', flat=True)
        years = [dob.year for dob in birth_years if dob]  # Extract year from each date
        birth_year_chart = px.histogram(
            x=years,
            nbins=30,
            labels={'x': 'Year of Birth', 'y': 'Number of Voters'},
            title="Distribution of Voters by Year of Birth"
        )
        context['birth_year_chart'] = mark_safe(pio.to_html(birth_year_chart, full_html=False))

        # Graph 2: Pie Chart of Voters by Party Affiliation
        party_counts = queryset.values('party_affiliation').annotate(count=models.Count('id'))
        party_affiliation_chart = px.pie(
            names=[party['party_affiliation'] for party in party_counts],
            values=[party['count'] for party in party_counts],
            title="Distribution of Voters by Party Affiliation"
        )
        context['party_affiliation_chart'] = mark_safe(pio.to_html(party_affiliation_chart, full_html=False))

        # Graph 3: Histogram of Voter Participation in Each Election
        election_data = {
            '2020 State Election': queryset.filter(v20state=True).count(),
            '2021 Town Election': queryset.filter(v21town=True).count(),
            '2021 Primary Election': queryset.filter(v21primary=True).count(),
            '2022 General Election': queryset.filter(v22general=True).count(),
            '2023 Town Election': queryset.filter(v23town=True).count(),
        }
        election_participation_chart = px.bar(
            x=list(election_data.keys()),
            y=list(election_data.values()),
            labels={'x': 'Election', 'y': 'Number of Voters'},
            title="Distribution of Voter Participation in Each Election"
        )
        context['election_participation_chart'] = mark_safe(pio.to_html(election_participation_chart, full_html=False))

        # Add form filter options for the template
        context['party_affiliations'] = Voter._meta.get_field('party_affiliation').choices
        context['years'] = range(1900, 2024)  # Range of years for date of birth filter
        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct().order_by('voter_score')

        return context