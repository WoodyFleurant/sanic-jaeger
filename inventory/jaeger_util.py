from jaeger_client import Config

def init_tracer(service):
    print("init_tracer")
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
            'reporter_batch_size': 1,
        },
        service_name=service,
    )

    # this call sets global variable opentracing.tracer
    config.initialize_tracer()