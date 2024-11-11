from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *

# Create your views here

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
    

    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'